import { ReactNode } from 'react';
import { cn } from '../../utils/cn';

type StatCardProps = {
  title: string;
  value: string | number;
  icon: ReactNode;
  change?: string;
  trend?: 'up' | 'down' | 'neutral';
  className?: string;
};

const StatCard = ({ title, value, icon, change, trend, className }: StatCardProps) => {
  return (
    <div className={cn(
      "bg-white rounded-xl shadow-soft p-6",
      className
    )}>
      <div className="flex justify-between items-start">
        <div>
          <p className="text-sm font-medium text-gray-500">{title}</p>
          <h3 className="mt-2 text-2xl font-semibold text-gray-900">{value}</h3>
          
          {change && (
            <div className="mt-2 flex items-center">
              <span
                className={cn(
                  "text-xs font-medium px-2 py-0.5 rounded",
                  trend === 'up' && "bg-success-100 text-success-800",
                  trend === 'down' && "bg-error-100 text-error-800",
                  trend === 'neutral' && "bg-gray-100 text-gray-800"
                )}
              >
                {change}
              </span>
            </div>
          )}
        </div>
        
        <div className="p-2 rounded-lg bg-primary-50 text-primary-700">
          {icon}
        </div>
      </div>
    </div>
  );
};

export default StatCard;