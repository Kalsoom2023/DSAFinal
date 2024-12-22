class AnimationSteps:
    def __init__(self):
        self.insertion_animation_steps = []
        self.current_insertion_step = None

    def add_insertion_step(self, original_index, final_index, key, step_count):
        self.insertion_animation_steps.append({
            'action': 'insert',
            'original_index': original_index,
            'final_index': final_index,
            'key': key,
            'step_count': step_count
        })
        self.current_insertion_step = self.insertion_animation_steps[-1]

    def add_probe_step(self, original_index, current_index, step_count):
        self.insertion_animation_steps.append({
            'action': 'probe',
            'original_index': original_index,
            'current_index': current_index,
            'step_count': step_count
        })
