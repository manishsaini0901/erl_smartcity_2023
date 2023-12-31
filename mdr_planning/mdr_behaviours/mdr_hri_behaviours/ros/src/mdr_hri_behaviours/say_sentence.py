import rospy
import random

from mas_execution_manager.scenario_state_base import ScenarioStateBase

class SaySentence(ScenarioStateBase):
    def __init__(self, save_sm_state=False, **kwargs):
        ScenarioStateBase.__init__(self, 'say_sentence',
                                   save_sm_state=save_sm_state,
                                   outcomes=['succeeded'])
        self.sm_id = kwargs.get('sm_id', '')
        self.state_name = kwargs.get('state_name', 'say_sentence')
        self.sentences = list(kwargs.get('sentences', list()))
        self.sleep_time = kwargs.get('sleep_time', -1.)

    def execute(self, userdata):
        sentence = random.choice(self.sentences)

        rospy.loginfo('Saying: %s' % sentence)
        self.say(sentence)

        if self.sleep_time > 0:
            rospy.sleep(self.sleep_time)
        return 'succeeded'
