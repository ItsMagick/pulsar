# Pulsar

Packes all dependencies of [pulsar](https://github.com/hgascon/pulsar) in a Docker image.

```sh
$ ./run --help
$ ./run -l -p dump.pcap
```

## From project README

Pulsar is a network fuzzer with automatic protocol learning and simulation
capabilites. The tool allows to model a protocol through machine learning
techniques, such as clustering, and Markov models. These models can be used to
simulate communication between Pulsar and a real client or server thanks to
semantically correct messages which, in combination with a series of fuzzing
primitives, allow to test the implementation of an unknown protocol for errors
in deeper states of its protocol state machine.
