fallback_model_output = """Hello, I am the fallback model. 

Can you spot me? 

```python
chain = prompt | ai_model.with_fallback([fallback_model]) | output_parser
```
                                                          
I am not an intelligent model. I always respond with the same text. 

I am writing to you because the primary model has failed. The following prompt was sent:

> Tell me a joke about bears.

But you didn't get a result from the OpenAI API endpoint it was passed to.

In all likelihood, the model name defined in the textbox above was not recognised by OpenAI. Or you have not entered a valid OpenAI API key in the left sidebar.

---

An example of a valid model name is 'gpt-3.5-turbo'.

---

But this is a good thing! It is my happy task to show you how the LangChain Expression Language (LCEL) can be used to

- configure a fallback model
- stream a model's response

---

### The LangChain Expression Language (LCEL)

The LangChain Expression Language (LCEL) has some nice features out-of-the-box:

- composability
- configurability
- observability
- streaming
- batching

--- 

Fallback is an example of out-of-the-box configurability. I'll show you the mechanism for introducing fallback onto a component of an LCEL-style chain very soon. It is also possible to apply fallback to an entire chain.

---

First, a chain of LCEL code looks like this:

```python
chain = componentA | componentB | ... | componentX
```

As you look at the LCEL chain, I suggest you keep in mind how any given component can be swapped out for another, or placed in a different position. For example, so long as it is logical to do so, you could re-compose the chain:

```python
chain = componentB | componentA | ... | componentX
```

Or introduce a new component:

```python
chain = componentA | componentAAA | componentB | ... | componentX
```

This should give you a sense of the composability of the LCEL. 

---

Second, to have an intuition for the configurability of the components in the chain, picture fluent interface method calls. 

That is, method chaining off an object with domain-specific method names:


```python
chain = componentA.with_something().with_another_thing() | ...
```

The above LCEL would apply the configurations of `with_something()` and `with_another_thing()` to `componentA`.

---

But let's get a bit more concrete and look at some actual code!

---

### Adding fallback to a component in the LCEL chain

```python
chain = prompt | ai_model.with_fallbacks([fallback_model]) | output_parser
```

Fallback was added by using the `with_fallback` method of the `ai_model` object.
To delegate to other models on failure, you simply pass a list of fallback models to try; in this case, just me!

### Adding streaming to the LCEL chain

```python
for chunk in chain.stream({{"topic": 'bears'}}):
    # code to dispatch chunk to the UI
```

Streaming was added to the chain through the `stream()` method; it is then 
treated as an iterator that yields data chunks as they become available. 

Using LCEL's out-of-the-box streaming makes it easy to dispatch chunks generated
by the model to the UI as soon as it becomes available.

For example, I'm processing chunks (characters in this case) with a delay of 
0.03 seconds between each character. This simulates the streaming of a computational model's response.


--- 

### The input to `stream()`

You may have noticed the dictionary passed to the `stream()` method. This is the input to the chain. `stream()` cascades a series of input-output events through the entire length of the chain and interacts with them like an iterator.

First, the cascade starts with input to the initial link in the chain. It then performs its core execution logic and produces an output.

Then that first output becomes input to the second link; in its turn, it executes its core execution logic and produces an output. That then becomes input to the next link in chain.

And so on.

---

### But what is `invoke()`?

If you have read some LCEL code before and seen `chain.invoke(...)`, you may be wondering about the difference between `invoke(input)` and `stream(input)`. 

`invoke` is the non-streaming mechanism to cascade input-output events through the length of the chain. Done that way, the output of the chain pops out all at once. This approach provides a poorer user experience.

--- 

"""   