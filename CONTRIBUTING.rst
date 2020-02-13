Contributing
============

I'm really glad you're reading this, because we need volunteer
developers to help this project come to fruition.

Data Compass is an open source project and we love to receive
contributions from our community — you! There are many ways to
contribute, from writing tutorials or blog posts, improving the
documentation, submitting bug reports and feature requests or writing
code which can be incorporated into Data Compass itself.

Following these guidelines helps to communicate that you respect the
time of the developers managing and developing this open source project.
In return, they should reciprocate that respect in addressing your
issue, assessing changes, and helping you finalize your pull requests.

These are mostly guidelines, not rules. Use your best judgment, and feel
free to propose changes to this document in a pull request.

Code of Conduct
---------------

Data Compass project has adopted a Code of Conduct that we expect
project participants to adhere to. Please read `the full text`_ so that
you can understand what actions will and will not be tolerated.

Open Development
----------------

All work on Data Compass happens directly on `GitHub`_. Both core team
members and external contributors send pull requests which go through
the same review process.

Branch Organization
-------------------

We will do our best to keep the |master branch|_ in good shape, with
tests passing at all times.

If you send a pull request, please do it against the |develop branch|_.

Semantic Versioning
-------------------

Data Compass follows `semantic versioning`_. We release patch versions
for bugfixes, minor versions for new features, and major versions for
any breaking changes.

Where to Find Known Issues
--------------------------

We are using `GitHub Issues`_ for all issues. Before filing a new task,
try to make sure your problem doesn't already exist.

Proposing a Change
------------------

If you intend to change the public API, or make any non-trivial changes
to the implementation, we recommend `filing an issue`_. This lets us
reach an agreement on your proposal before you put significant effort
into it.

If you're only fixing a bug, it's fine to submit a pull request right
away but we still recommend to file an issue detailing what you're
fixing. This is helpful in case we don't accept that specific fix but
want to keep track of the issue.

Your First Pull Request
-----------------------

Working on your first Pull Request? You can learn how from this free
video series:

`How to Contribute to an Open Source Project on GitHub`_

If you decide to fix an issue, please be sure to check the comment
thread in case somebody is already working on a fix. If nobody is
working on it at the moment, please leave a comment stating that you
intend to work on it so other people don't accidentally duplicate your
effort.

If somebody claims an issue but doesn't follow up for more than two
weeks, it's fine to take it over but you should still leave a comment.

Sending a Pull Request
----------------------

The core team is monitoring for pull requests. We will review your pull
request and either merge it, request changes to it, or close it with an
explanation. We'll do our best to provide updates and feedback
throughout the process.

Style Guide
-----------

Look at `Django Style Guide`_ will guide you in the right direction.

All python code should follow the `PEP 8 Style guide`_.

Our codebase utilizes `flake8`_, run the following command to make sure
your code fits our styling standards.

.. code:: sh

   $ flake8

Python imports are sorted using `isort`_.

.. code:: sh

   $ isort -rc .


URLs
~~~~

* List pages should use plurals; e.g. ``/projects/``, ``/surveys/``

* Detail pages should simply be a UUID/PK/slug on top of the list page; e.g.
  ``/projects/99e0dc36-a8f0-4a58-8f91-416d355125d5/``, ``/notifications/1/``
  ``/organizations/the-org/``

* Create pages should have 'create' as the final path segment; e.g.
  ``/notifications/create/``

* URL names use dashes.

* Update pages are sometimes the same as detail pages.
  In those cases, just use the detail convention, e.g.
  ``/projects/3/``.  If there is a distinction between the detail
  page and the update page, use ``/projects/3/update/``.

* Delete pages; e.g., ``/projects/3/delete/``

View class names
~~~~~~~~~~~~~~~~

Classes should be named according to::

    '{class_name}{verb}View'

For example, ``ProjectUpdateView``, ``ProjectCreateView``
``ProjectDeleteView``, ``ProjectListView`` and ``ProjectDetailView``.
This doesn't fit all situations, but it's a good basis.


Git Commit Guidelines
---------------------

We have very precise rules over how our git commit messages can be
formatted. This leads to **more readable messages** that are easy to
follow when looking through the **project history**. But also, we use
the git commit messages to **generate change log**.

Our codebase utilizes `Conventional Commits`_ specification.

Commit Message Format
~~~~~~~~~~~~~~~~~~~~~

Each commit message consists of a **header**, a **body** and a
**footer**. The header has a special format that includes a **type**, a
**scope** and a **subject**:

::

   <type>(<scope>): <subject>
   <BLANK LINE>
   <body>
   <BLANK LINE>
   <footer>

The **header** is mandatory and the **scope** of the header is optional.

Any line of the commit message cannot be longer 100 characters!. This
allows the message to be easier to read on GitHub as well as in various
git tools.

Revert
~~~~~~

If the commit reverts a previous commit, it should begin with
``revert:``, followed by the header of the reverted commit. In the body
it should say: ``This reverts commit <hash>.``, where the hash is the
SHA of the commit being reverted. A commit with this format is
automatically created by the |git revert|_ command.

Type
~~~~

Must be one of the following:

-  **feature**: A new feature
-  **fix**: A bug fix
-  **docs**: Documentation only changes
-  **style**: Changes that do not affect the meaning of the code
   (white-space, formatting, missing semi-colons, etc)
-  **refactor**: A code change that neither fixes a bug nor adds a
   feature
-  **performance**: A code change that improves performance
-  **test**: Adding missing or correcting existing tests
-  **build**: Changes to the build process or auxiliary tools and
   libraries such as documentation generation

Scope
~~~~~

The scope could be anything specifying place of the commit change. You
can use ``*`` when the change affects more than a single scope.

Subject
~~~~~~~

The subject contains succinct description of the change:

-  use the imperative, present tense: "change" not "changed" nor
   "changes"
-  don't capitalize first letter
-  no dot (.) at the end

Body
~~~~

Just as in the **subject**, use the imperative, present tense: "change"
not "changed" nor "changes". The body should include the motivation for
the change and contrast this with previous behavior.

Footer
~~~~~~

The footer should contain any information about **Breaking Changes** and
is also the place to `reference GitHub issues that this commit closes`_.

**Breaking Changes** should start with the word ``BREAKING CHANGE:``
with a space or two newlines. The rest of the commit message is then
used for this. A detailed explanation can be found in this `document`_.

License
-------

By contributing to Data Compass, you agree that your contributions will
be licensed under its license.

.. _developers-certificate-of-origin-11:

Developer's Certificate of Origin 1.1
-------------------------------------

By making a contribution to this project, I certify that:

-  (a) The contribution was created in whole or in part by me and I have
   the right to submit it under the open source license indicated in the
   file; or

-  (b) The contribution is based upon previous work that, to the best of
   my knowledge, is covered under an appropriate open source license and
   I have the right under that license to submit that work with
   modifications, whether created in whole or in part by me, under the
   same open source license (unless I am permitted to submit under a
   different license), as indicated in the file; or

-  (c) The contribution was provided directly to me by some other person
   who certified (a), (b) or (c) and I have not modified it.

-  (d) I understand and agree that this project and the contribution are
   public and that a record of the contribution (including all personal
   information I submit with it, including my sign-off) is maintained
   indefinitely and may be redistributed consistent with this project or
   the open source license(s) involved.

.. _the full text: https://github.com/IREXorg/data-compass/blob/develop/CODE_OF_CONDUCT.md
.. _GitHub: https://github.com/IREXorg/data-compass

.. |master branch| replace:: ``master`` branch
.. _master branch: https://github.com/IREXorg/data-compass/tree/master

.. |develop branch| replace:: ``develop`` branch
.. _develop branch: https://github.com/IREXorg/data-compass/tree/develop

.. _semantic versioning: http://semver.org/
.. _GitHub Issues: https://github.com/IREXorg/data-compass/issues
.. _filing an issue: https://github.com/IREXorg/data-compass/issues/new
.. _How to Contribute to an Open Source Project on GitHub: https://egghead.io/series/how-to-contribute-to-an-open-source-project-on-github
.. _Django Style Guide: https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/
.. _PEP 8 Style guide: https://www.python.org/dev/peps/pep-0008/
.. _flake8: https://pypi.org/project/flake8/
.. _isort: https://isort.readthedocs.io/en/latest/
.. _Conventional Commits: https://www.conventionalcommits.org/

.. |git revert| replace:: ``git revert``
.. _git revert: https://git-scm.com/docs/git-revert

.. _reference GitHub issues that this commit closes: https://help.github.com/articles/closing-issues-using-keywords/
.. _document: #commit-message-format
