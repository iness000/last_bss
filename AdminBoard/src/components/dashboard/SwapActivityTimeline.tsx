import { SwapActivity } from '../../context/DashboardContext';
import { Battery, Calendar, Clock, User, MapPin } from 'lucide-react';

type SwapActivityTimelineProps = {
  activities: SwapActivity[];
  limit?: number;
};

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date);
};

const SwapActivityTimeline = ({ activities, limit = 5 }: SwapActivityTimelineProps) => {
  // Sort activities by start_time, most recent first
  const sortedActivities = [...activities]
    .sort((a, b) => new Date(b.start_time).getTime() - new Date(a.start_time).getTime())
    .slice(0, limit);

  return (
    <div className="bg-white p-6 rounded-xl shadow-soft h-full">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Swap Activity</h3>
      
      {sortedActivities.length === 0 ? (
        <div className="text-center py-6 text-gray-500">No recent activities</div>
      ) : (
        <div className="space-y-4">
          {sortedActivities.map((activity) => (
            <div 
              key={activity.id} 
              className="p-4 rounded-lg border border-gray-100 hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center">
                  <div className={`w-2.5 h-2.5 rounded-full mr-2 ${
                    activity.status === 'active' ? 'bg-accent-500' : 'bg-success-500'
                  }`}></div>
                  <span className={`text-sm font-medium ${
                    activity.status === 'active' ? 'text-accent-700' : 'text-success-700'
                  }`}>
                    {activity.status === 'active' ? 'Active Swap' : 'Completed'}
                  </span>
                </div>
                <span className="text-xs text-gray-500">
                  ID: {activity.id}
                </span>
              </div>
              
              <div className="space-y-2">
                <div className="flex items-center text-sm">
                  <User size={16} className="text-gray-400 mr-2" />
                  <span className="text-gray-600">User {activity.user_id}</span>
                </div>
                
                <div className="flex items-center text-sm">
                  <Battery size={16} className="text-gray-400 mr-2" />
                  <span className="text-gray-600">Battery {activity.battery_in_id}</span>
                </div>
                
                <div className="flex items-center text-sm">
                  <MapPin size={16} className="text-gray-400 mr-2" />
                  <span className="text-gray-600">Station {activity.station_id}</span>
                </div>
                
                <div className="flex items-center text-sm">
                  <Calendar size={16} className="text-gray-400 mr-2" />
                  <span className="text-gray-600">{formatDate(activity.start_time)}</span>
                </div>
                
                {activity.end_time && (
                  <div className="flex items-center text-sm">
                    <Clock size={16} className="text-gray-400 mr-2" />
                    <span className="text-gray-600">{formatDate(activity.end_time)}</span>
                  </div>
                )}
                
                {activity.end_time && (
                  <div className="flex items-center text-sm">
                    <span className="text-gray-600">
                      Duration: {Math.round((new Date(activity.end_time).getTime() - new Date(activity.start_time).getTime()) / (1000 * 60))} min
                    </span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
      
      {activities.length > limit && (
        <div className="mt-4 text-center">
          <button className="text-primary-600 text-sm font-medium hover:text-primary-700">
            View all activity
          </button>
        </div>
      )}
    </div>
  );
};

export default SwapActivityTimeline;