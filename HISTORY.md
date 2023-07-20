Release History
===============

4.0.4 (2023-07-20)
------------------

### New Features

- Now that Actors can be called directly, present-tense aliases have been added for all Actions.

### Improvements

- Some extra indentation left over from The Before Days have finally been removed. Thanks to the eagle-eyes of @bandophahita for noticing them!

4.0.3 (2022-09-18)
------------------

### New Features

- Targets are now able to be created without an explicit name, like `Target().located_by(...)`. A Target created this way will use the locator string to describe itself. You'll be able to save some coding space and reduce repetition! (h/t @bandophahita!)
- Now Questions which catch an exception (e.g. `Element`) will store any exceptions which they encounter, which will allow reporting of those caught exceptions. This is particularly useful when `Element` doesn't find the element, so you can inspect the actual exception message. (h/t @bandophahita!)

### Improvements

- Massive improvement in code covered by unit tests! (h/t @bandophahita!)
- Cleanup, dependency updates, and more!

4.0.2 (2022-05-13)
------------------

### New Features

- Added `IsPresent` and `IsInvisible` Resolutions, thanks @bandophahita!

### Improvements

- Lots of type hinting improvements to improve your IDE experience. Thanks again, @bandophahita!

4.0.1 (2022-02-22)
------------------

In honor of 2sday, how about 2 deploys?

### Bugfixes

- Fix some issues with dependencies (hopefully), so installing via `screenpy[selenium]` works.

4.0.0 (2022-02-22)
------------------

2day is 2sday, by the way. Also I pushed this up at 22:22!

### Timeline

- Broke off from ScreenPy's core library, https://github.com/ScreenPyHQ/screenpy!
