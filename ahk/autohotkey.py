from collections import deque

from ahk.keyboard import KeyboardMixin, AsyncKeyboardMixin
from ahk.mouse import MouseMixin, AsyncMouseMixin
from ahk.registry import RegistryMixin, AsyncRegistryMixin
from ahk.screen import ScreenMixin, AsyncScreenMixin
from ahk.sound import SoundMixin, AsyncSoundMixin
from ahk.window import WindowMixin, AsyncWindowMixin
from ahk.gui import GUIMixin, AsyncGUIMixin


class AHK(WindowMixin, MouseMixin, KeyboardMixin, ScreenMixin, SoundMixin, RegistryMixin, GUIMixin):
    """
    Inherits its methods from the following classes:

    | :py:class:`ahk.window.WindowMixin`
    | :py:class:`ahk.mouse.MouseMixin`
    | :py:class:`ahk.keyboard.KeyboardMixin`
    | :py:class:`ahk.screen.ScreenMixin`
    | :py:class:`ahk.sound.SoundMixin`
    | :py:class:`ahk.registery.RegisteryMixin`
    | :py:class:`ahk.gui.GUIMixin`
    """

    pass


#
class AsyncAHK(
    AsyncMouseMixin,
    AsyncKeyboardMixin,
    AsyncWindowMixin,
    AsyncScreenMixin,
    AsyncSoundMixin,
    AsyncRegistryMixin,
    AsyncGUIMixin,
):
    ...


class ActionChain(AHK):
    """
    Reusable action chain to execute various actions in order
    """

    def __init__(self, *args, **kwargs):
        self._actions = deque()
        super().__init__(*args, **kwargs)

    def run_script(self, *args, **kwargs):
        """
        override run_script to defer to queue
        """
        kwargs['decode'] = False  #
        self._actions.appendleft((args, kwargs))

    def perform(self):
        results = []
        while self._actions:
            args, kwargs = self._actions.pop()
            results.append(super().run_script(*args, **kwargs))
        return results

    def sleep(self, n):
        """
        :param n: how long (in seconds) to sleep
        :return:
        """
        n = n * 1000  # convert to milliseconds
        script = self.render_template(
            'base.ahk',
            body=f'Sleep {n}',
            directives={
                '#Persistent',
            },
        )
        self.run_script(script)
