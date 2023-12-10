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

# CS242 Week 2 - Lambda Calculus

!!! abstract
    The lecture note in the website is very clear and condensed. However, the knowledge is organized in an intuitive instead of a neat way. Here I will try to list some important points for reference and some really intuitive pick-ups.

<!-- more -->

!!! info
    course version: 2019-fall

    course website: [:octicons-book-16:](https://stanford-cs242.github.io/f19/lectures/02-1-lambda-calculus)

    my assignment: [:octicons-mark-github-16:]()


## Operational Semantics

=== "D-Lam"

    $$\frac{\ }{\bf{\lambda} x . e \bf{val}}$$

    <center> Functions are values.

=== "D-App-Step"

    $$\frac{e_{lam} \mapsto e_{lam}'}{e_{lam} \ e_{arg} \mapsto e_{lam}' \ e_{arg}}$$

    <center>Step the left expression $e_{lam}$ until it becomes a function.

=== "D-App-Sub"

    $$\frac{\ }{(\bf{\lambda} x . e_{lam}) \ e_{arg} \mapsto [x \rightarrow e_{arg}]\ e_{lam}}$$

    <center>replace all free variables x in $e_{lam}$ with $e_{arg}$.

## Main Idea

1. Understanding lambda calculus as an extendable and analyzable language. The following class could be abstracted as extending lambda calculus with some PL theories.
2. To prove that we have enumerated all the edge cases, we need to prove the safety of the program after we prevent the renumerated cases.
