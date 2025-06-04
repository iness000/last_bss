import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { Battery } from '../../context/DashboardContext';

type BatteryHealthChartProps = {
  batteries: Battery[];
};

const BatteryHealthChart = ({ batteries }: BatteryHealthChartProps) => {
  // Calculate battery health distribution
  const calculateHealthData = () => {
    const healthRanges = [
      { name: 'Excellent (90-100%)', range: [90, 100], color: '#10B981' },
      { name: 'Good (80-89%)', range: [80, 89], color: '#34D399' },
      { name: 'Fair (70-79%)', range: [70, 79], color: '#FBBF24' },
      { name: 'Poor (60-69%)', range: [60, 69], color: '#F97316' },
      { name: 'Critical (<60%)', range: [0, 59], color: '#EF4444' },
    ];

    return healthRanges.map(range => {
      const count = batteries.filter(
        battery => {
          const health = battery.latest_soh_percent || 0; // Use latest_soh_percent, fallback to 0
          return health >= range.range[0] && health <= range.range[1];
        }
      ).length;

      return {
        name: range.name,
        value: count,
        color: range.color
      };
    });
  };

  const data = calculateHealthData();

  return (
    <div className="bg-white p-6 rounded-xl shadow-soft h-full">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Battery Health Overview</h3>
      
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={80}
              paddingAngle={5}
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip 
              formatter={(value) => [`${value} batteries`, '']}
              contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)' }}
            />
            <Legend layout="vertical" verticalAlign="middle" align="right" />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default BatteryHealthChart;