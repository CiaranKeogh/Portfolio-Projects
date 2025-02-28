import React from 'react';
import { communityStats, CommunityStatItem, CommunityActivity, Contributor } from '@/data/community';

export function CommunityStatsSection() {
  return (
    <section className="py-16 bg-gunmetal">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-off-white mb-4">
            Join Our Community
          </h2>
          <p className="text-off-white/80 max-w-2xl mx-auto">
            War Thunder Tactics is more than just a resource - it's a thriving community
            of players sharing strategies and helping each other improve.
          </p>
        </div>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-16">
          {communityStats.stats.map((stat: CommunityStatItem, index: number) => (
            <div key={index} className="bg-deep-blue/40 rounded-lg p-6 text-center">
              <div className="text-4xl font-bold text-burnt-orange mb-2">
                {stat.value}
              </div>
              <div className="text-off-white/80 text-sm">{stat.label}</div>
            </div>
          ))}
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
          {/* Recent Activity */}
          <div>
            <h3 className="text-2xl font-bold text-off-white mb-6">
              Recent Activity
            </h3>
            <div className="space-y-4">
              {communityStats.recentActivity.slice(0, 3).map((activity: CommunityActivity, index: number) => (
                <div key={index} className="bg-deep-blue/20 rounded-lg p-4">
                  <div className="flex items-center mb-2">
                    <div className="w-10 h-10 rounded-full mr-3 bg-olive-drab/60 flex items-center justify-center text-off-white font-medium">
                      {activity.userName.charAt(0)}
                    </div>
                    <div>
                      <div className="text-off-white font-medium">{activity.userName}</div>
                      <div className="text-off-white/60 text-xs">{activity.time}</div>
                    </div>
                  </div>
                  <p className="text-off-white/80 text-sm">{activity.action}</p>
                  <div className="mt-3 text-xs">
                    <a href={activity.link} className="text-burnt-orange hover:text-burnt-orange/80">
                      View details →
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          {/* Top Contributors */}
          <div>
            <h3 className="text-2xl font-bold text-off-white mb-6">
              Top Contributors
            </h3>
            <div className="bg-deep-blue/20 rounded-lg p-6">
              <div className="space-y-4">
                {communityStats.topContributors.slice(0, 5).map((contributor: Contributor, index: number) => (
                  <div key={index} className="flex items-center justify-between">
                    <div className="flex items-center">
                      <div className="w-10 h-10 rounded-full mr-3 bg-deep-blue/60 flex items-center justify-center text-off-white font-medium">
                        {contributor.name.charAt(0)}
                      </div>
                      <div>
                        <div className="text-off-white font-medium">{contributor.name}</div>
                        <div className="text-off-white/60 text-xs">{contributor.contributions} contributions</div>
                      </div>
                    </div>
                    <div className="flex items-center">
                      <div className="text-burnt-orange font-bold mr-2">{index + 1}</div>
                      <div className="w-16 h-2 bg-gunmetal rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-burnt-orange" 
                          style={{ width: `${(contributor.score / communityStats.topContributors[0].score) * 100}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              <div className="mt-6 text-center">
                <a 
                  href="/community" 
                  className="inline-block bg-olive-drab hover:bg-olive-drab/90 text-off-white font-medium py-2 px-6 rounded transition-colors"
                >
                  Join the Community
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
} 