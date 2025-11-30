import { useState } from 'react';

interface SearchBarProps {
  onSearch: (query: string) => void;
  isSearching?: boolean;
  placeholder?: string;
}

export default function SearchBar({ 
  onSearch, 
  isSearching = false,
  placeholder = "Search for similar items..." 
}: SearchBarProps) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="relative">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={placeholder}
          disabled={isSearching}
          className="w-full px-4 py-3 pl-12 bg-white/10 border border-emerald-400/30 rounded-lg text-emerald-50 placeholder-emerald-200/50 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent disabled:opacity-50"
        />
        <div className="absolute left-4 top-1/2 -translate-y-1/2">
          <svg
            className="h-5 w-5 text-emerald-300"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            />
          </svg>
        </div>
        <button
          type="submit"
          disabled={isSearching || !query.trim()}
          className="absolute right-2 top-1/2 -translate-y-1/2 px-4 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-md transition-all disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium"
        >
          {isSearching ? 'Searching...' : 'Search'}
        </button>
      </div>
    </form>
  );
}

