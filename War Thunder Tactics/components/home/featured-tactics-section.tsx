import { TacticCard } from '@/components/tactics/tactic-card';
import { Section } from '@/components/ui/section';
import { getFeaturedTactics } from '@/lib/tactics-utils';

export function FeaturedTacticsSection() {
  const tactics = getFeaturedTactics(4);
  
  return (
    <Section
      title="Featured Tactics"
      description="Discover the most effective strategies created by the community"
      viewAllLink="/tactics"
      viewAllText="Browse All Tactics"
    >
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {tactics.map((tactic, index) => (
          <TacticCard 
            key={tactic.id} 
            tactic={tactic} 
            featured={index === 0} 
          />
        ))}
      </div>
    </Section>
  );
} 