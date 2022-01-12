import luigi
import time
import os


class MakeDirectory(luigi.Task):
    path = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(self.path)

    def run(self):
        os.makedirs(self.path)


class HelloTask(luigi.Task):
    path = luigi.Parameter()

    def run(self):
        with open(self.path, 'w') as hello_file:
            hello_file.write('Hello')
            hello_file.close()

    def output(self):
        return luigi.LocalTarget(self.path)

    def requires(self):
        return [MakeDirectory(path=os.path.dirname(self.path))]


class WorldTask(luigi.Task):
    path = luigi.Parameter()

    def run(self):
        time.sleep(10)
        with open(self.path, 'w') as world_file:
            world_file.write('World')
            world_file.close()

    def output(self):
        return luigi.LocalTarget(self.path)

    def requires(self):
        return [MakeDirectory(path=os.path.dirname(self.path))]


class HelloWorldTask(luigi.Task):
    id = luigi.Parameter(default='test')

    def run(self):
        with open(self.input()[0].path, 'r') as hello_file:
            hello = hello_file.read()
        with open(self.input()[1].path, 'r') as world_file:
            world = world_file.read()
        with open(self.output().path, 'w') as output_file:
            content = "{} {}".format(hello, world)
            output_file.write(content)
            output_file.close()

    def requires(self):
        return [
            HelloTask('results/{}/hello.txt'.format(self.id)),
            WorldTask('results/{}/hello.txt'.format(self.id))
        ]

    def output(self):
        path = 'results/{}/hello_world.txt'.format(self.id)
        return luigi.LocalTarget(path)


if __name__ == "__main__":
    luigi.run()
