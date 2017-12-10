#include <ros/ros.h>
#include <sensor_msgs/Joy.h>
#include <std_msgs/Float64MultiArray.h>

#define MAX_LIN_SPEED 230
#define MAX_ANGLE 30
#define MAX_ANGLE_BR 80


ros::Publisher control_pub;

void joyCallback(const sensor_msgs::Joy::ConstPtr& joy) {

	std::vector<float> axe = joy -> axes;
	std::vector<int> but = joy -> buttons;
	
	std::vector<double> out(8, 0);

	////////////DriveSpeed////////////

	out[0] = MAX_LIN_SPEED * axe[1];

	////////////SteeringAngle////////////

	out[1] = - MAX_ANGLE * axe[3];
	
	////////////BaseRotation////////////
	
	out[2] =  - MAX_ANGLE_BR * axe[7];

	////////////ShoulderActuator////////////
	
	if( but[0] == 1)
		{
			out[3] = -1;	
		}
	else if ( but[3] == 1)
		{	
			out[3] = 1;	
		}
	else {out[3] = 0;}

	////////////Elbow Actuator////////////

	if( but[4] == 1)
		{
			out[4] = -1;	
		}
	else if ( but[5] == 1)
		{	
			out[4] = 1;	
		}
	else {out[4] = 0;}


	////////////PitchMotor////////////
	
	out[5]=0
	
	////////////RollMotor////////////
	
	out[6] = axe[6];

	////////////GripperMotor////////////
	
	if( axe[2] == -1)
		{
			out[7] = -1;	
		}
	else if ( axe[5] == -1)
		{	
			out[7] = 1;	
		}
	else {out[7] = 0;}

	std_msgs::Float64MultiArray outMsg;
	outMsg.data = out;
	control_pub.publish(outMsg);
}

int main(int argc, char** argv) {

	ros::init(argc, argv, "joystick_driver");
	ros::NodeHandle _nh;
	
	control_pub = _nh.advertise<std_msgs::Float64MultiArray>("/rover/control_directives", 100);
	ros::Subscriber joy_sub = _nh.subscribe("/joy", 100, joyCallback);
	ros::Rate loop_rate(100);

	ros::spin();

	return 0;
}
