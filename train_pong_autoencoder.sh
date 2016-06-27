#!/usr/bin/env sh

./build/tools/caffe train \
  --solver=examples/mnist/pong_autoencoder_solver.prototxt
