============
Deprecations
============

This page documents
the major deprecations
in ScreenPy Selenium's life,
and how to adjust your tests
to keep them up to date.

4.1.0 Deprecations
==================

Boolean Positional Arguments Deprecation
----------------------------------------

The following class constructors 
have been marked deprecated 
when using a positional boolean argument in the constructor. 
Starting with version 5.0.0
you will be required to provide keywords 
for the following boolean arguments.

:class:`~screenpy_selenium.actions.enter.Enter`

Before::

    the_actor.will(Enter("foo", True).into_the(PASSWORD))

After::

    the_actor.will(Enter("foo", mask=True).into_the(PASSWORD))


:class:`~screenpy_selenium.actions.hold_down.HoldDown`

Before::

    the_actor.will(Chain(HoldDown(None, True))

After::

    the_actor.will(Chain(HoldDown(None, lmb=True))
    the_actor.will(Chain(HoldDown(lmb=True))
    

:class:`~screenpy_selenium.actions.release.Release`

Before::

    the_actor.will(Release(None, True))

After::

    the_actor.will(Release(None, lmb=True))
    the_actor.will(Release(lmb=True))


:class:`~screenpy_selenium.questions.selected.Selected`

Before::

    the_actor.shall(See.the(Selected(TARGET, True), IsEmpty()))

After::

    the_actor.shall(See.the(Selected(TARGET, multi=True), IsEmpty()))


:class:`~screenpy_selenium.questions.text.Text`

Before::

    the_actor.shall(See.the(Text(TARGET, True), IsEqual("foo"))

After::

    the_actor.shall(See.the(Text(TARGET, multi=True), IsEqual("foo")


