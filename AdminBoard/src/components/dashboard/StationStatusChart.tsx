import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Station } from '../../context/DashboardContext';

type StationStatusChartProps = {
  stations: Station[];
};

const StationStatusChart = ({ stations }: StationStatusChartProps) => {
  // Transform station data for the chart
  const chartData = stations.map(station => {
    // Ensure values are numbers, defaulting to 0 if not.
    const totalSlots = Number(station.total_slots) || 0;
    const availableSlots = Number(station.available_slots) || 0;
    
    // Calculate active batteries. Ensure it's not negative if data is inconsistent.
    const activeBatteries = Math.max(0, totalSlots - availableSlots);

    return {
      name: station.name,
      capacity: totalSlots,      // Use total_slots for the station's capacity
      active: activeBatteries,   // Calculated: total_slots - available_slots
      available: availableSlots, // Use available_slots directly
      status: station.status,
    };
  });

  return (
    <div className="bg-white p-6 rounded-xl shadow-soft h-full">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Station Capacity Utilization</h3>
      
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={chartData}
            margin={{ top: 5, right: 30, left: 0, bottom: 20 }}
            barGap={0}
            barCategoryGap="20%"
          >
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f5f5f5" />
            <XAxis 
              dataKey="name" 
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 12 }}
            />
            <YAxis 
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 12 }}
              allowDecimals={false}
            />
            <Tooltip 
              cursor={{ fill: 'rgba(0, 0, 0, 0.05)' }}
              contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)' }}
            />
            <Bar 
              dataKey="active" 
              stackId="a" 
              fill="#4338CA" 
              name="Active Batteries" 
              radius={[4, 4, 0, 0]}
            />
            <Bar 
              dataKey="available" 
              stackId="a" 
              fill="#A5B4FC" 
              name="Available Slots" 
              radius={[4, 4, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default StationStatusChart;