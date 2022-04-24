# Contributing to Luso

:tada: First off, thank you for considering contributing to Luso! :tada:

All members of our community are expected to follow
our [Code of Conduct](CODE_OF_CONDUCT.md).
Please make sure you are welcoming and friendly in all of our spaces.

The following is a set of guidelines for contributing to Luso. Feel free to propose
changes to this document in a pull request.

# Contributions

There a variety of ways in which you can contribute. Here are some of the areas where
we would really appreciate your contribution:

* [Source Code](#source-code)
    * [Issues](#issues)
    * [Pull Requests](#pull-requests)
* [Discussions](#discussions)
    * Feature Requests & Ideas
    * Q & A
    * Community participation
* [Content](#content)
    * Resources
    * Artwork

# Source Code

## Issues

Issues are created [here](https://github.com/luso-me/luso/issues/new).

### How to Contribute in Issues

For any issue, there are fundamentally three ways an individual can contribute:

1. By opening the issue for discussion: If you believe that you have found a new bug in
   Luso, you should report it by creating a new issue
   [here](https://github.com/luso-me/luso/issues/new).

2. By helping to triage the issue: You can do this either by providing assistive
   details (a reproducible test case that demonstrates a bug) or by providing suggestions
   to address the issue.

3. By helping to resolve the issue: This can be done by demonstrating that the issue is
   not a bug or is fixed; but more often, by opening a pull request that changes the
   source in luso.me/luso repository in a concrete and reviewable manner.

### Asking for General Help

[Where can I get more help?](README.md#where-can-i-get-more-help) has a list of resources 
for getting programming help, reporting security issues, contributing, and more. 

Please use the [issue tracker](https://github.com/luso-me/luso/issues) for bugs only!

### Submitting a Bug Report

When opening a new issue in the issue tracker, users will be presented
with a template that should be filled in.

If you believe that you have found a bug in Luso, please fill out the template to the
best of your ability.

The two most important pieces of information needed to evaluate the report are a
description of the bug and a simple test case to recreate it. It is easier to fix a bug if
it can be reproduced.

See [How to create a Minimal, Complete, and Verifiable example.](https://stackoverflow.com/help/minimal-reproducible-example)

### Triaging a Bug Report

It's common for open issues to involve discussion. Some contributors may have differing
opinions, including whether the behavior is a bug or feature. This discussion is part of
the process and should be kept focused, helpful, and professional.

Terse responses that provide neither additional context nor supporting detail are not
helpful or professional. To many, such responses are annoying and unfriendly.

Contributors are encouraged to solve issues collaboratively and help one another make
progress. If you encounter an issue that you feel is invalid, or which contains incorrect
information, explain why you feel that way with additional supporting context, and be
willing to be convinced that you may be wrong. By doing so, we can often reach the correct
outcome faster.

### Resolving a Bug Report

Most issues are resolved by opening a pull request. The process for opening and reviewing
a pull request is similar to that of opening and triaging issues, but carries with it a
necessary review and approval workflow that ensures that the proposed changes meet the
minimal quality and functional guidelines of the Luso project.

## Pull Requests

Pull Requests are the way concrete changes are made to the code, documentation,
dependencies, and tools contained in the `luso.me/luso` repository.

* [Setting up your local environment](#setting-up-your-local-environment)
    * [Prerequisites](#prerequisites)
    * [Step 1: Fork](#step-1-fork)
    * [Step 2: Build](#step-2-build)
    * [Step 3: Branch](#step-3-branch)
* [Making Changes](#making-changes)
    * [Step 4: Code](#step-4-code)
    * [Step 5: Commit](#step-5-commit)
        * [Commit message guidelines](#commit-message-guidelines)
    * [Step 6: Rebase](#step-6-rebase)
    * [Step 7: Test](#step-7-test)
    * [Step 8: Push](#step-8-push)
    * [Step 9: Opening the Pull Request](#step-9-opening-the-pull-request)
    * [Step 10: Discuss and Update](#step-10-discuss-and-update)
        * [Approval and Request Changes Workflow](#approval-and-request-changes-workflow)
    * [Step 11: Landing](#step-11-landing)
    * [Continuous Integration Testing](#continuous-integration-testing)

### Setting up your local environment

#### Prerequisites

* Docker (for Mongo)
  * `docker run --name lusodb --rm -d -p 27017:27017 mongo:4.4.6`
* Python >= 3.9.
* Node.js >= 14.

#### Step 1: Fork

Fork the project [on GitHub](https://github.com/luso.me/luso) and clone your fork
locally.

```sh
$ git clone git@github.com:username/luso.git
$ cd luso
$ git remote add upstream https://github.com/luso.me/luso.git
$ git fetch upstream
```

#### Step 2: Build

TODO

#### Step 3: Branch

To keep your development environment organized, create local branches to
hold your work. These should be branched directly off of the `master` branch.

```sh
$ git checkout -b my-branch -t upstream/master
```

### Making Changes

#### Step 4: Code

TODO

#### Step 5: Commit

It is recommended to keep your changes grouped logically within individual
commits. Many contributors find it easier to review changes that are split
across multiple commits. There is no limit to the number of commits in a
pull request.

```sh
$ git add my/changed/files
$ git commit
```

Note that multiple commits get squashed when they are landed.

##### Commit message guidelines

A good commit message should describe what changed and why. Luso
uses [semantic commit messages](https://conventionalcommits.org/) to streamline
the release process.

Before a pull request can be merged, it **must** have a pull request title with a semantic
prefix.

Examples of commit messages with semantic prefixes:

* `fix: server returns incorrect error to client`
* `feat: add ability to delete a skill`
* `docs: add additional community channels to README.md`

Common prefixes:

* fix: A bug fix
* feat: A new feature
* docs: Documentation changes
* test: Adding missing tests or correcting existing tests
* build: Changes that affect the build system
* ci: Changes to our CI configuration files and scripts
* perf: A code change that improves performance
* refactor: A code change that neither fixes a bug nor adds a feature
* style: Changes that do not affect the meaning of the code (linting)

Other things to keep in mind when writing a commit message:

1. The first line should:
    * contain a short description of the change (preferably 50 characters or less,
      and no more than 72 characters)
    * be entirely in lowercase with the exception of proper nouns, acronyms, and
      the words that refer to code, like function/variable names
2. Keep the second line blank.
3. Wrap all other lines at 72 columns.


