#!/bin/bash

../src/protobuf/bin/protoc  -I=../src/proto --cpp_out=../src/proto/cpp_out --python_out=./python_out ../src/proto/*.proto

echo "success"