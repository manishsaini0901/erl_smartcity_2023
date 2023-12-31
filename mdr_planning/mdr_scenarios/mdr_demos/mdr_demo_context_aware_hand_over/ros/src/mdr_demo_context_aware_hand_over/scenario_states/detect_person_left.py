import rospy
import actionlib
import moveit_commander
from mdr_find_people.msg import FindPeopleAction, FindPeopleGoal
from mas_execution_manager.scenario_state_base import ScenarioStateBase
from geometry_msgs.msg import Twist
import math

class DetectPerson(ScenarioStateBase):
    def __init__(self, save_sm_state=False, **kwargs):
        ScenarioStateBase.__init__(self, 'detect_person_left',
                                   save_sm_state=save_sm_state,
                                   outcomes=['succeeded', 'failed', 'failed_after_retrying'],
                                   output_keys=['person_list','person_location'],
                                   input_keys=['person_location'])
        self.sm_id = kwargs.get('sm_id', 'mdr_demo_context_aware_hand_over')
        self.action_server = kwargs.get('action_server', 'find_people_server')
        self.timeout = kwargs.get('timeout', 120.)
        self.twist_msg = Twist()
        self.person_location = kwargs.get('person_location', None)
        self.number_of_retries = kwargs.get('number_of_retries', 0)
        self.retry_count = 0
        self.client = actionlib.SimpleActionClient(self.action_server, FindPeopleAction)
        self.client.wait_for_server(rospy.Duration(10.))
        self.base_vel_pub = rospy.Publisher ('/hsrb/command_velocity', Twist, queue_size=1)
        

    def execute(self, userdata):      
        # Set velocity command values
        self.twist_msg.linear.x = 0
        self.twist_msg.linear.y = 0
        #self.twist_msg.angular.z = 100 / 180.0 * math.pi # Convert from "degree" to "radian"
        #self.base_vel_pub.publish (self.twist_msg) # Publish velocity command

        self.twist_msg.angular.z=0.3
        for i in range(110):
            self.base_vel_pub.publish (self.twist_msg) # Publish velocity command
            rospy.sleep(0.1)

        goal = FindPeopleGoal()
        # calling the actionlib server and waiting for the execution to end
        rospy.loginfo('[detect_person] Sending action lib goal to {0}'.format(self.action_server))
        self.say('Detecting people')
        self.client.send_goal(goal)
        self.client.wait_for_result(rospy.Duration.from_sec(int(self.timeout)))
        result = self.client.get_result()

        if result and result.person_list.persons:
            rospy.loginfo('[detect_person] Found {0} people'.format(len(result.person_list.persons)))
            userdata.person_list = result.person_list
            userdata.person_location=self.person_location
            return 'succeeded'
        else:
            rospy.logerr('Could not detect a person')
            self.say('Could not detect a person')
            if self.retry_count == self.number_of_retries:
                self.say('Aborting operation')
                return 'failed_after_retrying'
            self.retry_count += 1
            return 'failed'

    
