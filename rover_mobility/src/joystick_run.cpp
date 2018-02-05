#include <ros/ros.h>
#include <sensor_msgs/Joy.h>
#include <std_msgs/Float64MultiArray.h>

#define MAX_LIN_SPEED 230
#define MAX_ANGLE 30


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
	
	if( but[5] == 1)
		{
			out[2] = -1;	
		}
	else if ( but[4] == 1)
		{	
			out[2] = 1;	
		}
	else {out[2] = 0;}

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

	if( axe[7] == 1)
		{
			out[4] = 1;	
		}
	else if ( axe[7] == -1)
		{	
			out[4] = -1;	
		}
	else {out[4] = 0;}


	////////////PitchMotor////////////
	
	if( axe[6] == 1)
		{
			out[5] = 1;	
		}
	else if ( axe[6] == -1)
		{	
			out[5] = -1;	
		}
	else {out[5] = 0;}
	
	////////////RollMotor////////////
	
	if( but[1] == 1)
		{
			out[6] = 1;	
		}
	else if ( but[2] == 1)
		{	
			out[6] = -1;	
		}
	else {out[6] = 0;}

	////////////GripperMotor////////////
	
	if( axe[2] == -1)
		{
			out[7] = 1;	
		}
	else if ( axe[5] == -1)
		{	
			out[7] = -1;	
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
