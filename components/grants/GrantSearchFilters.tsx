import React, { useState } from 'react';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';

interface GrantFilters {
  keyword: string;
  agency: string;
  category: string;
  minAmount: string;
  maxAmount: string;
  deadline: string;
}

interface GrantSearchFiltersProps {
  onSearch: (filters: GrantFilters) => void;
  onReset: () => void;
}

export const GrantSearchFilters: React.FC<GrantSearchFiltersProps> = ({
  onSearch,
  onReset
}) => {
  const [filters, setFilters] = useState<GrantFilters>({
    keyword: '',
    agency: '',
    category: '',
    minAmount: '',
    maxAmount: '',
    deadline: ''
  });

  const handleChange = (field: keyof GrantFilters, value: string) => {
    setFilters(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(filters);
  };

  const handleReset = () => {
    setFilters({
      keyword: '',
      agency: '',
      category: '',
      minAmount: '',
      maxAmount: '',
      deadline: ''
    });
    onReset();
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow-md space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Keywords
        </label>
        <Input
          type="text"
          placeholder="Search grants by keyword..."
          value={filters.keyword}
          onChange={(e) => handleChange('keyword', e.target.value)}
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Agency
          </label>
          <select
            className="w-full border border-gray-300 rounded-md px-3 py-2"
            value={filters.agency}
            onChange={(e) => handleChange('agency', e.target.value)}
          >
            <option value="">All Agencies</option>
            <option value="NSF">National Science Foundation</option>
            <option value="NIH">National Institutes of Health</option>
            <option value="DOE">Department of Energy</option>
            <option value="USDA">US Department of Agriculture</option>
            <option value="DOD">Department of Defense</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Category
          </label>
          <select
            className="w-full border border-gray-300 rounded-md px-3 py-2"
            value={filters.category}
            onChange={(e) => handleChange('category', e.target.value)}
          >
            <option value="">All Categories</option>
            <option value="research">Research</option>
            <option value="education">Education</option>
            <option value="infrastructure">Infrastructure</option>
            <option value="technology">Technology</option>
            <option value="health">Health</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Min Amount ($)
          </label>
          <Input
            type="number"
            placeholder="0"
            value={filters.minAmount}
            onChange={(e) => handleChange('minAmount', e.target.value)}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Max Amount ($)
          </label>
          <Input
            type="number"
            placeholder="Any"
            value={filters.maxAmount}
            onChange={(e) => handleChange('maxAmount', e.target.value)}
          />
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Deadline Before
        </label>
        <Input
          type="date"
          value={filters.deadline}
          onChange={(e) => handleChange('deadline', e.target.value)}
        />
      </div>

      <div className="flex gap-2 pt-2">
        <Button type="submit" variant="primary" className="flex-1">
          Search Grants
        </Button>
        <Button type="button" variant="outline" onClick={handleReset}>
          Reset
        </Button>
      </div>
    </form>
  );
};
