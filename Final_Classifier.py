from functionality import classify
from absl import app
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_enum('model', 'GB', ['GB', 'SVM'], 'ML Classfier', short_name='c')

def main(argv):
    wave = input("Name of a wav-file:") + ".wav"
    print(classify(wave, FLAGS.model), f"(using {FLAGS.model} model)")

if __name__ == '__main__':
  app.run(main)