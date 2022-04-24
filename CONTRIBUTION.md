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
* Discussions
    * Feature Requests & Ideas
    * Q & A
    * Community participation
* Content
    * Resources
    * Artwork

# Source Code

## Technologies Used

* Website: [Svelte](https://svelte.dev/) / [TypeScript](https://www.typescriptlang.org/)
* Server: [Python](https://www.python.org/)
* Database: [Mongo](https://www.mongodb.com/)

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
    * poetry
* Node.js >= 14.
    * yarn

#### Tutorial

If you have never created a pull request before, welcome :tada:. [Here is a great
tutorial](https://app.egghead.io/playlists/how-to-contribute-to-an-open-source-project-on-github)
on how to create a pull request.

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

##### Website

- create .env file in the `website/` directory and set the following env variables:

```
API_URL=http://localhost:5000
ROLLUP_WATCH=true
```

##### Server

- create .env file in the `server/` directory and set the following env variables:

```shell
MONGO_CONNECTION_URL=mongodb://localhost:27017
GITHUB_CLIENT_ID=<github client id> (see notes on how to find it)
GITHUB_CLIENT_SECRET=<github client secret> (see notes on how to find it)
TOKEN_SECRET_KEY=<any random string> (see notes on how to generate)
ICONS_S3_BUCKET=mybucket
ICONS_S3_BUCKET_REGION=eu-west-1
```

- To activate the virtual env from your shell
  ```
  poetry shell
  ```
- To find GITHUB_CLIENT_ID do ...
- To find GITHUB_CLIENT_SECRET do ...
- TOKEN_SECRET_KEY generation
  ```shell
  openssl rand -hex 32
  ```

#### Step 3: Branch

To keep your development environment organized, create local branches to
hold your work. These should be branched directly off of the `master` branch.

```sh
$ git checkout -b my-branch -t upstream/master
```

### Making Changes

#### Step 4: Code

Most pull requests opened against this repository include changes to either the Python
code in the `server/` directory, the TypeScript/Svelte code in the `website/` directory
or the documentation in `docs/` directory.

Please be sure to run the following linters from time to on any code changes to ensure
that you follow the project's code style:

* For Python - run `black` in the `server/` directory.
* For TypeScript/Svelte - run `npm run lint` in the `website/` directory.

See coding style for more information about best practice when modifying code in different
parts of the project.

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

### Step 6: Rebase

Once you have committed your changes, it is a good idea to use `git rebase`
(not `git merge`) to synchronize your work with the repository.

```sh
$ git fetch upstream
$ git rebase upstream/master
```

This ensures that your working branch has the latest changes from `luso.me/luso` master.

### Step 7: Test

#### Website

##### create local config

name: cypress.env.json

content:

```json
{
  "baseUrl": "http://localhost:7000",
  "jwtAccessToken": "<get_valid_jwt_token_from_svelte_store>",
  "userId": "<your_user_id>"
}
```

```sh
$/website> npm run test
```

Make sure the linter does not report any issues and that all tests pass. Please do not 
submit patches that fail either check.

##### Server

```sh
$/server> pytest tests
```

### Step 8: Push

Once your commits are ready to go **_with passing tests and linting_**
begin the process of opening a pull request by pushing your working branch
to your fork on GitHub.

```sh
$ git push origin my-branch
```

### Step 9: Opening the Pull Request

From within GitHub, opening a new pull request will present you with a template
that should be filled out. It can be found
[here](https://github.com/luso.me/luso/blob/master/.github/PULL_REQUEST_TEMPLATE.md).

If you do not adequately complete this template, your PR may be delayed in being merged as
maintainers seek more information or clarify ambiguities.

### Step 10: Discuss and update

You will probably get feedback or requests for changes to your pull request.
This is a big part of the submission process so don't be discouraged! Some
contributors may sign off on the pull request right away. Others may have
detailed comments or feedback. This is a necessary part of the process
in order to evaluate whether the changes are correct and necessary.

To make changes to an existing pull request, make the changes to your local
branch, add a new commit with those changes, and push those to your fork.
GitHub will automatically update the pull request.

```sh
$ git add my/changed/files
$ git commit
$ git push origin my-branch
```

There are a number of more advanced mechanisms for managing commits using
`git rebase` that can be used, but are beyond the scope of this guide.

Feel free to post a comment in the pull request to ping reviewers if you are
awaiting an answer on something. If you encounter words or acronyms that
seem unfamiliar, refer to this [glossary](docs/glossary.md).

#### Approval and Request Changes Workflow

Whenever a maintainer reviews a pull request they may request changes. These may be
small, such as fixing a typo, or may involve substantive changes. Such requests are
intended to be helpful, but at times may come across as abrupt or unhelpful, especially
if they do not include concrete suggestions on *how* to change them.

Try not to be discouraged. If you feel that a review is unfair, say so or seek
the input of another project contributor. Often such comments are the result of
a reviewer having taken insufficient time to review and are not ill-intended.
Such difficulties can often be resolved with a bit of patience. That said,
reviewers should be expected to provide helpful feedback.

### Step 11: Landing

In order to land, a pull request needs to be reviewed and approved by
at least one Maintainer and pass CI. After that, if there are no
objections from other contributors, the pull request can be merged.

Congratulations and thanks for your contribution!

### Continuous Integration Testing

Every pull request is tested on the Continuous Integration (CI) system to confirm that
it works.

Ideally, the pull request will pass ("be green") on GitHub actions.
This means that all tests pass and there are no linting errors.
Each CI failure must be manually inspected to determine the cause.

CI starts automatically when you open a pull request, but only
core maintainers can restart a CI run. If you believe CI is giving a
false negative, ask a maintainer to restart the tests.

## Other Items

### Style Guides

These are the style guidelines for coding in Luso.

#### General Code

* End files with a newline.
* Place requires in the following order:
  * Built in Node Modules (such as path)
  * Local Modules (using relative paths)
* Place class properties in the following order:
  * Class methods and properties (methods starting with a @)
  * Instance methods and properties
* Avoid platform-dependent code:
  * Use path.join() to concatenate filenames.
  * Use os.tmpdir() rather than /tmp when you need to reference the temporary directory.
* Using a plain return when returning explicitly at the end of a function.
  * Not return null, return undefined, null or undefined

#### Python

For Python, we follow the `black` Coding Style. 

#### Typescript

For TypeScript, we have both:
* a formatter which you can run with `npm run prelint`.
* a linter which you can run with `npm run lint`.

### Versions

Version numbers consists of a major version, minor version and a release number. For
more info see [SemVer](http://semver.org).

All version tags starts with “v”, so version 0.8.0 has the tag v0.8.0.

### Feature branches

Major new features are worked on in dedicated branches. There's no strict naming
requirement for these branches.

Feature branches are removed once they've been merged into a release branch.

### Tags

- Tags are used exclusively for tagging releases. A release tag is
  named with the format ``vX.Y.Z`` -- for example ``v2.3.1``.

- Experimental releases contain an additional identifier ``vX.Y.Z-id`` --
  for example ``v3.0.0-rc1``.

- Experimental tags may be removed after the official release.
