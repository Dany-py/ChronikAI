"""
ChronikAI — Point d'entrée principal
Lance le watcher en arrière-plan et prépare le démarrage de studio.
"""

import threading
import signal
import sys
from apps.watcher import Tracker


def start_watcher(stop_event: threading.Event):
    """Lance le Tracker dans un thread dédié."""
    tracker = Tracker(
        replay=True,
        duration=60,
        verbose=True,
        idle_threshold=1,
    )

    # Arrêt propre quand stop_event est déclenché
    def watch():
        while not stop_event.is_set():
            tracker.run_session()

    watch()


def main():
    print("ChronikAI v1.0.0 — démarrage...")

    stop_event = threading.Event()

    # Watcher dans un thread daemon (s'arrête avec le process principal)
    watcher_thread = threading.Thread(
        target=start_watcher,
        args=(stop_event,),
        name="watcher",
        daemon=True,
    )
    watcher_thread.start()
    print("[watcher] actif")

    # Studio : pas encore implémenté
    # studio_thread = threading.Thread(target=start_studio, daemon=True)
    # studio_thread.start()
    print("[studio]  en attente d'implémentation")

    # Gestion Ctrl+C propre
    def on_exit(sig, frame):
        print("\nArrêt demandé...")
        stop_event.set()
        sys.exit(0)

    signal.signal(signal.SIGINT, on_exit)
    signal.signal(signal.SIGTERM, on_exit)

    # Maintenir le process principal en vie
    watcher_thread.join()


if __name__ == "__main__":
    main()