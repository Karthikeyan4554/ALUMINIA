import React from 'react';

interface AvatarProps {
  name?: string;
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl';
  className?: string;
  role?: string;
}

const sizeClasses = {
  xs: 'w-6 h-6 text-[10px]',
  sm: 'w-8 h-8 text-xs',
  md: 'w-10 h-10 text-sm',
  lg: 'w-12 h-12 text-base',
  xl: 'w-16 h-16 text-xl',
  '2xl': 'w-20 h-20 text-2xl',
  '3xl': 'w-24 h-24 text-3xl',
};

// Deterministic pleasing palette for initials
const colorPalettes = [
  'bg-gradient-to-br from-indigo-500 to-indigo-700 text-white shadow-xs',
  'bg-gradient-to-br from-blue-500 to-blue-700 text-white shadow-xs',
  'bg-gradient-to-br from-violet-500 to-violet-700 text-white shadow-xs',
  'bg-gradient-to-br from-teal-500 to-teal-700 text-white shadow-xs',
  'bg-gradient-to-br from-emerald-500 to-emerald-700 text-white shadow-xs',
  'bg-gradient-to-br from-rose-500 to-rose-700 text-white shadow-xs',
  'bg-gradient-to-br from-amber-500 to-amber-700 text-white shadow-xs',
  'bg-gradient-to-br from-cyan-500 to-cyan-700 text-white shadow-xs',
];

export const getInitials = (name?: string): string => {
  if (!name || !name.trim()) return 'U';
  // Strip honorifics like Dr., Prof.
  const cleaned = name.replace(/^(Dr\.|Prof\.|Mr\.|Ms\.|Mrs\.)\s+/i, '').trim();
  const parts = cleaned.split(/\s+/).filter(Boolean);
  if (parts.length === 0) return 'U';
  if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
};

export const Avatar: React.FC<AvatarProps> = ({
  name = 'User',
  size = 'md',
  className = '',
  role,
}) => {
  const initials = getInitials(name);

  // Simple deterministic hash based on name string
  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  }
  const colorIndex = Math.abs(hash) % colorPalettes.length;
  const palette = colorPalettes[colorIndex];

  return (
    <div
      className={`inline-flex items-center justify-center font-bold tracking-tight select-none rounded-full shrink-0 border border-white/20 ${sizeClasses[size]} ${palette} ${className}`}
      title={name}
      aria-label={name}
    >
      <span>{initials}</span>
    </div>
  );
};

export default Avatar;
