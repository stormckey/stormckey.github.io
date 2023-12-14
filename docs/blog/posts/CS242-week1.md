---
comments: true
authors:
    - stormckey
categories:
    - CS242
    - PL
date: 2023-12-09
nostatistics: true
draft: true
---

# CS242 Week 1 - Syntax and Semantics

!!! abstract
    The lecture note in the website is very clear and condensed. However, the knowledge is organized in an intuitive instead of a neat way. Here I will try to list some important points for reference and some really intuitive pick-ups.

<!-- more -->

!!! info
    course version: 2019-fall

    course website: [:octicons-book-16:](https://stanford-cs242.github.io/f19/lectures/01-2-syntax-semantics)

    my assignment: [:octicons-book-github-16:](https://github.com/stormckey/CS242-PL/blob/master/assign1/written/assign1.pdf)

## The Idea of Backus's paper

The first reading assignment was the paper of Backus,"Can programming be liberated from the von Neumann style?: a functional style and its algebra of programs". I did not read through the whole paper but I have finished half of it.

The main idea of the paper, I think, is that Backus tried to liberate the programmers from the laborious work required by Von Neumann languages, where programmers are busy handling the irrelevant details like memory management, variable assignment, nested control flow etc. So he proposed a new kind of system where no variable, assignment and history is needed. He gave the definition of the system and showed some convenient properties of the system such as we can analyse and transform the program in a algebra-like way.

That's where I have read to. And as a student 50 years after the publication of the paper, I can conclude that the so said Von Neumann languages are still the mainstream today and the underlying hardware implementation is also monopolized by the Von Neumann architecture.

I'm skeptical whether the method proposed by Backus a actually a better way, as all the laborious work seems also necessary to be done some way if we dont come up with a brand new architecture. And the ability to control this details may be necessay to control the computer efficiently, which is obviously an advantage over functional languages.

So is the mechanism of Non Von Neumann languages really a practical and better way? How much power can it unleash? The answer remains unkonwn, at least to me.(Maybe this is problem that has already been solved somewhere)

## Induction

Lecture 1.2 validate the induction for natual numbers, here are things that I think is important:

- every natual number is either 0 or a successor of natual number. So our case is exhaustive.
- For any given n, we need always to find its predecessor until we find 0, the process of which will always terminate in finite steps.
- This rule applies to other structures. So a good way to help us untangle our proof mechanism is to write down the structure.

## Operational Semantics

Here some quotations from TAPL which I think describe the operational semantics very well:

> Operational semantics specifies the behavior of a programming language by defining a simple abstract machine for it.

> For simple languages, a state of the machine is just a term, and the machine’s behavior is defined by a transition function that, for each state, either gives the next state by performing a step of simplification on the term or declares that the machine has halted.

> The intuition is that, if t is the state of the abstract machine at a given moment, then the machine can make a step of computation and change its state to t′.
