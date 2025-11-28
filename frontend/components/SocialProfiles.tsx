import { User } from 'lucide-react';

interface SocialProfilesProps {
  socialHandles: Record<string, string[]>;
}

export default function SocialProfiles({ socialHandles }: SocialProfilesProps) {
  const hasProfiles = Object.values(socialHandles).some(handles => handles.length > 0);

  return (
    <div className="bg-gradient-to-br from-neutral-900/60 to-neutral-900/40 border border-neutral-800 rounded-2xl p-6 backdrop-blur-sm hover:border-neutral-700 transition-all duration-300">
      <div className="flex items-center gap-3 mb-4">
        <div className="p-2 bg-purple-500/10 rounded-lg">
          <User className="w-5 h-5 text-purple-400" />
        </div>
        <h3 className="font-semibold text-white">Social Profiles</h3>
        <span className="ml-auto text-xs font-medium text-neutral-500 bg-neutral-800/50 px-2 py-1 rounded">
          {Object.values(socialHandles).reduce((acc, handles) => acc + handles.length, 0)}
        </span>
      </div>
      <div className="space-y-3 max-h-64 overflow-y-auto custom-scrollbar">
        {hasProfiles ? (
          Object.entries(socialHandles).map(([platform, handles]) => (
            handles.length > 0 && (
              <div key={platform} className="bg-neutral-950/50 rounded-lg p-3 border border-neutral-800/50">
                <div className="text-xs text-neutral-500 uppercase mb-2 font-medium">{platform}</div>
                <div className="flex flex-wrap gap-2">
                  {handles.map((handle, i) => (
                    <span key={`${platform}-${handle}-${i}`} className="text-sm text-neutral-300 bg-neutral-800/70 px-2.5 py-1 rounded-md hover:bg-neutral-800 transition-colors">
                      @{handle}
                    </span>
                  ))}
                </div>
              </div>
            )
          ))
        ) : (
          <div className="text-neutral-500 text-sm italic text-center py-4">No profiles found</div>
        )}
      </div>
    </div>
  );
}
