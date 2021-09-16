# Future features


## support for multiple sequences in one run

This way one could bundle a set of sequences into one run without reinstantiating `factory` and `Seshu`.

* change `command line parser` to take in a list of sequence names
* change `SequenceProvider`'s `get_sequence` to take `sequence_name` as argument
* change `SequenceRunner`
  * `add_step` to take the additional parameter `sequence_name`
  * `run` to take additional parameter `sequence_name`
  * add `sequences` dict, which holds a multitude of sequences with their corresponding steps


### Questions on the changes above

Should the factories fully initialize themselves befor getting passed to `Seshu`? Potential errors, like the `reading of configs` and instantiation of the `Steps` would also happen befor getting passed.

Is it `Seshu`'s responisibility to handle `Factory` errors? No, its the factory which is responsible, and if there are errors, like reading a `sequence` or `step` config, the factory shouldn't get passed to `Seshu`.

This way, the factory should also include the logging's `baseConfig` initialization, or get it's own log handler. No, separate logfiles would make reading logs more complicated. One log for everything, one for tests is good enough here.


## support for conditional steps

Imagine three steps, A, B and C. And let's say, either B or C gets called depending on the result of A. How would one model this? In a tree-like structure!

This would require different implementations of `provider` and `runner` and another type sequence. Like `"type": "conditional-sequence"`. But probably doable without changing the `Seshu` logic.


## support for sequence chaining and conditional sequence selection

Not only excute sequences in order, but as with steps, let the output of the former sequence be the input for the latter. Plus conditional chaining. So a step can either have a step or sequence as successor.