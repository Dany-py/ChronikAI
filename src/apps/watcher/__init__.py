
"""
User activity tracking module
Monitors keyboard/mouse activity and records text typed in active application windows.
"""

from pynput import mouse, keyboard
from colorama import Fore, Style
import pywinctl as pw
import time

class Tracker:
    """
    Main class for user activity tracking.
    
    Monitors keyboard/mouse interactions and records text typed
    in each active application window.
    
    Attributes:
        win_activity (dict): Dictionary storing activity by window
        current_phrase (str): Currently typed phrase
        active_window_id (str): Unique ID of currently active window
        active_window_title (str): Title of currently active window
        last_activity (float): Timestamp of last detected activity
        mouse_listener (mouse.Listener): Mouse event listener
        autosave_threshold (int): Character count before auto-save
    """
    
    def __init__(self, idle_threshold = 1, verbose = False, blacklist_app = [],
                  duration = 10, replay = False, autosave_threshold = 100):
        """
        Initialize the activity tracker.
        
        Args:
            idle_threshold (int): Idle threshold in seconds
            verbose (bool): Enable/disable debug messages
            blacklist_app (list): List of applications not to track
            duration (int): Default tracker activity duration
            replay (bool): Enable/disable automatic tracker restart after delay
            autosave_threshold (int): Character count before automatic save
        """
        
        self.win_activity = {}
        self.current_phrase = ""
        self.active_window_id = "Unknown"
        self.active_window_app = "Unknown"
        self.active_window_title = "Unknown"
        self.last_activity = time.time()
        self.idle_threshold = idle_threshold
        self.verbose = verbose
        self.blacklist_app = blacklist_app
        self.duration = duration
        self.replay = replay
        self.autosave_threshold = autosave_threshold
        self.char_count= 0
        self.is_running = False
        self.should_stop = False

    def _update_activity(self, *args):
        """Update timestamp of last detected activity."""
        self.last_activity = time.time()

    def generate_window_id(self, title):
        """
        Generate a unique ID for a given window.
        
        Args:
            title (str): Window title
        
        Returns:
            str: Unique generated ID for the window
        """
        return f"{title}_{hash(title)}"

    def on_press(self, key):
        """
        Keyboard key press event handler.
        
        Captures alphanumeric characters and handles special keys
        (Space, Backspace, Enter) to build the current phrase.
        
        Args:
            key: pynput Key object representing the pressed key
        """
        self._update_activity()

        # Periodic auto-save
        if len(self.current_phrase) >=0:
            self.save_activity()
            self.current_phrase = ""

        try:
            # Capture standard alphanumeric characters
            if hasattr(key, 'char') and key.char is not None:
                self.current_phrase += key.char
                self.char_count += 1
                
                if self.char_count >= self.autosave_threshold:
                    if self.verbose:
                        print(f"[AUTO-SAVE] : {self.char_count} characters reached, auto-saving...")
                    self.save_activity()
                    self.current_phrase = ""
                    self.char_count = 0

        except AttributeError:
            pass
        
        # Handle special keys
        if key == keyboard.Key.space:
            self.current_phrase += " "
            
        elif key == keyboard.Key.backspace:
            self.current_phrase = self.current_phrase[:-1]
        
        elif key == keyboard.Key.tab:
            self.current_phrase += "[TAB]"
        
        elif key == keyboard.Key.esc:
            print("\n[ESC] Stop requested...")
            if self.current_phrase.strip():
                self.save_activity()
            self.should_stop = True

        elif key == keyboard.Key.enter:
            if self.current_phrase.strip():
                self.save_activity()
                print(f"[{self.active_window_title}] : {self.current_phrase}")
                self.current_phrase = ""

    def save_activity(self):
        """
        Save current phrase to activity dictionary.
        
        Creates new entry for window if needed, and adds
        typed text to the text list for that window.
        Filters certain control characters (Ctrl+C, Ctrl+T).
        """

        splided_app_name = self.active_window_app.split('.')[0] if self.active_window_app else "Unknown"
        window_id = splided_app_name + '_' + self.generate_window_id(int(time.time()))
        title = self.active_window_title
        text_to_save = self.current_phrase
        blacklist = self.blacklist_app
        
        # Initialize window entry if first occurrence
        if window_id not in self.win_activity and title not in blacklist:
            self.win_activity[window_id] = {
                'app_name': self.active_window_app,
                'title' : self.active_window_title,
                'timestamp': time.time(),
                'end': 0,
                'duration': 0,
                'consulted': True,
                'write': False,
                'text': [],
                'char_total': 0
            }
        
        # Filter control characters and add text
        # \x03 = Ctrl+C, \x14 = Ctrl+T
        if text_to_save != '' and text_to_save != '\x03' and text_to_save != '\x14':
            self.win_activity[window_id]['text'].append(text_to_save)
            self.win_activity[window_id]['write'] = True
            self.win_activity[window_id]['char_total'] += len(text_to_save)
            self.win_activity[window_id]['end'] = time.time()

            duration = self.win_activity[window_id]['end'] - self.win_activity[window_id]['timestamp']
            self.win_activity[window_id]['duration'] = int(duration)            
        else:
            self.win_activity[window_id]['text'].append('')
            self.win_activity[window_id]['write'] = False
            self.win_activity[window_id]['end'] = time.time()

            duration = self.win_activity[window_id]['end'] - self.win_activity[window_id]['timestamp']
            self.win_activity[window_id]['duration'] = int(duration)

    def get_idle_time(self):
        """
        Calculate idle duration in seconds.
        
        Returns:
            float: Seconds since last detected activity
        """
        return time.time() - self.last_activity

    def get_activity_data(self):
        """
        Return collected activity data.
        
        Returns:
            dict: Dictionary of activities by window
        """
        return self.win_activity.copy()

    def clear_activity_data(self):
        """Reset activity data."""
        self.win_activity = {}

    def stop(self):
        """Save remaining data and stop tracking."""
        if self.current_phrase.strip():
            self.save_activity()
        self.is_running = False
        self.mouse_listener.stop()
        self.kb_listener.stop()

    def run_session(self):
        """
        Launch main monitoring loop.
        
        Starts keyboard/mouse listeners, monitors active window changes
        and detects idle periods. Continues until interrupted by Ctrl+C.
        """

        self.mouse_listener = mouse.Listener(
            on_move=self._update_activity, 
            on_click=self._update_activity,
            on_scroll=self._update_activity
        )
        
        self.is_running = True
        start_session_time = time.time()
        self.kb_listener = keyboard.Listener(on_press=self.on_press)
    
        # Start listeners
        self.mouse_listener.start()
        self.kb_listener.start()

        if self.verbose:
            print("=" * 60)
            print("Monitoring active... (ESC or Ctrl+C to stop)")
            print(f"- Auto-save every {self.autosave_threshold} characters")
            print(f"- Session duration: {self.duration}s")
            print("=" * 60)
        
        try:
            while time.time() - start_session_time < self.duration and not self.should_stop:
                # Get currently active window
                try:
                    window = pw.getActiveWindow()
                    if window is not None:
                        new_window_id = self.generate_window_id(window.title)
                        new_app_name = window.getAppName()
                        new_window_title = window.title  
                except:
                    time.sleep(0.2)             
                    continue

                # Detect active window change
                if self.active_window_id != new_window_id:
                    if self.current_phrase.strip():
                        if self.verbose:
                            print(f"\n[WINDOW CHANGE] Saving before change")
                        self.save_activity()
                        self.current_phrase = ""
                        self.char_count = 0
                    
                    # Update active window
                    self.active_window_title = new_window_title
                    self.active_window_app = new_app_name
                    self.active_window_id = new_window_id
                    self.save_activity()
                    if self.verbose:
                        print(f"\n[ACTIVE] {new_app_name} - {new_window_title}")

                # Check idle time
                idle_duration = self.get_idle_time()
                if idle_duration > self.idle_threshold:
                    if self.current_phrase.strip():
                        if self.verbose:
                            print(f"\n[IDLE] Saving after {int(idle_duration)}s of inactivity")
                        self.save_activity()
                        self.current_phrase = ""
                        self.char_count = 0
                    
                    if self.verbose:
                        print(f"Status: Idle ({int(idle_duration)}s)", end="\r")
                
                time.sleep(0.2)
                
        except KeyboardInterrupt:
            if self.verbose:
                print("\n" + "=" * 60)
                print("\nStopping... Summary:")
                print(f"Activity summary: {self.win_activity}")
            self.should_stop = True
        except Exception as e:
            print(f"\n⚠ Unexpected error: {e}")
            self.should_stop = True
        finally:
            self.stop()
            if self.verbose:
                print("\n" + "=" * 60)
                print("SESSION SUMMARY:")
                print(f"\n\n- Monitored windows: {len(self.win_activity)}")
                total_chars = sum(w.get('char_total', 0) for w in self.win_activity.values())
                print(f'\n\n- Saved data: {self.win_activity}')
                print(f"\n\n- Captured characters: {total_chars}")
                print("=" * 60)

    def run(self):
        """Launch tracker in loop if 'replay' is True."""
        i = 1
        while self.replay and not self.should_stop:
            print(f"\n{'='*60}")
            print(f"Start n°{i}")
            print(f"{'='*60}")
            self.run_session()
            i += 1

        if not self.replay:
            self.run_session()
        

if __name__ == "__main__":
    warning = """
╔═══════════════════════════════════╗
║         TRACKER WARNING           ║
╚═══════════════════════════════════╝

⚠️  ETHICAL AND LEGAL WARNING ⚠️:
    This software captures keyboard strokes and mouse movements.
    If you use it on your machine, it is with full knowledge
    and consent.
    
    Legitimate uses only:
    - Self-monitoring (your own machine)
    - Research with informed consent
    - Transparent parental control

"""

    print(Fore.RED)
    print(f'{warning}')
    print(Style.RESET_ALL)
    
    tracker = Tracker(replay=True, duration=60, verbose=True)
    tracker.run()