# Imports
import time
import sys
import numpy as np


# %%
def breath_animation(
    animation_duration=30,
    inhale_symbol="O",
    exhale_symbol=".",
    inhale_seconds=5,
    exhale_seconds=5,
    field_width=70,
):
    """

    Parameters
    ----------
    animation_duration : int
        Number of seconds in the animation
    inhale_symbol : char
        The character symbol for inhaling
    exhale_symbol : char
        The character symbol for exhaling
    inhale_seconds : int
        Number of seconds per inhale
    exhale_seconds : int
        Number of seconds per exhale
    field_width : int
        The number of characters in the inhale/exhale print field

    Returns
    -------
    None
    """

    inhale_marker_times = np.linspace(0, inhale_seconds, field_width)
    inhale_symbol_num = np.ceil(
        (np.sin(np.linspace(-np.pi / 2, np.pi / 2, field_width)) + 1) * field_width / 2
    )

    exhale_marker_times = np.linspace(
        inhale_seconds, inhale_seconds + exhale_seconds, field_width
    )
    exhale_symbol_num = inhale_symbol_num * -1 + field_width  # Inverse Signal

    start_time = time.time()
    diff_time = time.time() - start_time
    mod_time = diff_time % inhale_seconds
    previous_marker_time = 0

    breath_status = "inhale"
    print_ready = False

    while diff_time <= animation_duration:

        if breath_status == ">>> INHALE >>>":

            marker_time = np.where(inhale_marker_times >= mod_time)[0][0]

            if marker_time > previous_marker_time:
                inhale_num = int(inhale_symbol_num[marker_time])
                exhale_num = field_width - inhale_num
                print_ready = True
                previous_marker_time = marker_time

            diff_time = time.time() - start_time
            mod_time = diff_time % (inhale_seconds + exhale_seconds)

            if mod_time > inhale_seconds:
                breath_status = "<<< exhale <<<"
                previous_marker_time = 0

        else:
            marker_time = np.where(exhale_marker_times >= mod_time)[0][0]

            if marker_time > previous_marker_time:
                inhale_num = int(exhale_symbol_num[marker_time])
                exhale_num = field_width - inhale_num
                print_ready = True
                previous_marker_time = marker_time

            diff_time = time.time() - start_time
            mod_time = diff_time % (inhale_seconds + exhale_seconds)

            if mod_time < inhale_seconds:
                breath_status = ">>> INHALE >>>"
                previous_marker_time = 0

        if print_ready:
            state = inhale_symbol * inhale_num + exhale_symbol * exhale_num
            output_string = breath_status + " [" + state + "] " + breath_status
            sys.stdout.write("\r" + output_string)
            sys.stdout.flush()
            print_ready = False

    return


#%%
if __name__ == "__main__":
    breath_animation()
