# Ray-tune example for LRBench
# Modified from https://github.gatech.edu/kyeom6/CS-6220-Project

# ray
import ray
from ray import tune
from ray.tune.schedulers import FIFOScheduler

# LRBench
from LRBench.lr.LR import LR

import os
import argparse
from filelock import FileLock

# Training configurations
EPOCH_SIZE = 512
TEST_SIZE = 256

# Wrapper class
class ConfigurableNet:
    def __init__(self):
        self.tune = tune
        self.dl = None
        self.nn = None
        self.dataloader = None
        self.config = None
        self.optim = None
        self.dataset = None
        self.transforms = None
        self.data_path = None
    def set_space(self, dl, net, config, optim):
        self.dl = dl
        self.net = net
        self.config = config
        self.optim = optim

    def data_loader(self, dataloader, dataset, transforms, data_path):
        self.dataloader = dataloader
        self.dataset = dataset
        self.transforms = transforms
        self.data_path = data_path

    def load_data(self):
        transform = self.transforms.Compose(
            [self.transforms.ToTensor(),
             self.transforms.Normalize((0.1307, ), (0.3081, ))])

        # Add FileLock here because multiple workers will want to
        # download data, and this may cause overwrites since
        # DataLoader is not threadsafe.
        with FileLock(os.path.expanduser(f"{self.data_path}.lock")):
            train_loader = self.dataloader(
                self.dataset(
                    self.data_path,
                    train=True,
                    download=True,
                    transform=transform),
                batch_size=self.config['batch_size'],
                shuffle=True)
            test_loader = self.dataloader(
                self.dataset(
                    self.data_path,
                    train=False,
                    download=True,
                    transform=transform),
                batch_size=self.config['batch_size'],
                shuffle=True)
        return train_loader, test_loader

    def __train__(self, model, optimizer, train_loader, device):
        device = device
        model.train()
        for batch_idx, (data, target) in enumerate(train_loader):
            if batch_idx * len(data) > EPOCH_SIZE:
                return
            data, target = data.to(device), target.to(device)
            optimizer.zero_grad()
            output = model(data)
            loss = self.dl.nn.functional.nll_loss(output, target)
            loss.backward()
            optimizer.step()

    def test(self, model, data_loader, device):
        device = device
        model.eval()
        correct = 0
        total = 0
        with self.dl.no_grad():
            for batch_idx, (data, target) in enumerate(data_loader):
                if batch_idx * len(data) > TEST_SIZE:
                    break
                data, target = data.to(device), target.to(device)
                outputs = model(data)
                _, predicted = self.dl.max(outputs.data, 1)
                total += target.size(0)
                correct += (predicted == target).sum().item()

        return correct / total

    def train(self, config):
        use_cuda = self.dl.cuda.is_available()
        device = self.dl.device("cuda" if use_cuda else "cpu")
        train_loader, test_loader = self.load_data()
        model = self.net.to(device)

        optimizer = self.optim.Adadelta(model.parameters(), lr=config["lr_scale"])

        # Set initial learning rate for FIX condition
        lrbench_config = {**config['lr_policy'], **{'k0':config['lr_scale']}} \
                        if config['lr_policy']['lrPolicy'] == 'FIX' else config['lr_policy']
        lrbenchLR = LR(lrbench_config)
        i = 1
        while True:
            self.__train__(model, optimizer, train_loader, device)
            acc = self.test(model, test_loader, device)
            # Update learning rate
            for param_group in optimizer.param_groups:
                param_group['lr'] = lrbenchLR.getLR(i - 1)

            # Termination condition for POLY
            if config['lr_policy']['lrPolicy'] == 'POLY':
                if i == config['lr_policy']['l']+1:
                    return

            i += 1
            # Set this to run Tune.
            self.tune.report(mean_accuracy=acc)

    def print_Dict(self, dictionary_item):
        for key, value in dictionary_item.items():
            space = len(str(value))
            print(f"{key}: {value}", end="\t")
            if space < 5:
                print("\t", end="")
        print("")

    def change_report(self, idx, dictionary_item):
        result = dict()
        result['rank'] = idx
        for key, value in dictionary_item['config'].items():
            if key != 'user_option':
                result[key] = value
        return result

    def report(self, analysis, config=None):
        report = list(analysis.results.values())
        best_config = None
        if config is not None:
            if 'user_option' in config:
                if 'accuracy_threshold' in config['user_option']:
                    report = [item for item in report if item['mean_accuracy'] > config['user_option']['accuracy_threshold']]
                    report = sorted(report, key = lambda item: item['time_total_s'])
                else:
                    report = sorted(report, key = lambda item: item['mean_accuracy'], reverse=True)
                if 'head' in config['user_option']:
                    report = report[:config['user_option']['head']]
        if len(report) == 0:
            print("No results satisfying the user options") 
            return
        best_config = report[0]['config']
        report = [self.change_report(idx, item) for idx, item in enumerate(report)]
        for item in report:
            self.print_Dict(item)
        return best_config

    def run(self):
        parser = argparse.ArgumentParser(description="PyTorch MNIST Example")
        parser.add_argument(
            "--cuda",
            action="store_true",
            default=False,
            help="Enables GPU training")
        parser.add_argument(
            "--smoke-test", action="store_true", help="Finish quickly for testing")
        parser.add_argument(
            "--ray-address",
            help="Address of Ray cluster for seamless distributed execution.")
        parser.add_argument(
            "--server-address",
            type=str,
            default=None,
            required=False,
            help="The address of server to connect to if using "
            "Ray Client.")
        args, _ = parser.parse_known_args()

        if args.server_address:
            ray.init(f"ray://{args.server_address}")
        elif args.ray_address:
            ray.init(address=args.ray_address)
        else:
            ray.shutdown()
            ray.init(num_cpus=2 if args.smoke_test else None)

        sched = FIFOScheduler()

        analysis = self.tune.run(
            lambda cfg: self.train(cfg),
            metric="mean_accuracy",
            mode="max",
            name="exp",
            scheduler=sched,
            stop={
                "training_iteration": self.config["stop_iteration"]
            },
            resources_per_trial={
                "cpu": 2,
                "gpu": int(args.cuda)  # set this for GPUs
            },
            num_samples=1 if args.smoke_test else 1,
            config=self.config)

        best_config = self.report(analysis, self.config)
        print("\nBest config is: ", best_config)
