import { Section } from '@/components/ui/section';
import { TacticData, featuredTactics } from '@/lib/tactics-utils';
import Image from 'next/image';
import Link from 'next/link';

export function CommunityHighlightSection() {
  // Get the top tactic for the highlight
  const highlightedTactic: TacticData = featuredTactics[0];
  
  return (
    <Section
      title="Community Highlight"
      description="Featured strategy from our top contributors"
      className="bg-deep-blue/20"
    >
      <div className="bg-gunmetal rounded-lg overflow-hidden shadow-lg">
        <div className="grid grid-cols-1 lg:grid-cols-5">
          {/* Left side - Image */}
          <div className="lg:col-span-3 relative">
            <div className="aspect-w-16 aspect-h-9 lg:h-full relative">
              <Image
                src={highlightedTactic.previewImage}
                alt={highlightedTactic.title}
                fill
                className="object-cover"
              />
              
              {/* Map name badge */}
              <div className="absolute top-4 left-4 bg-gunmetal/80 rounded-full px-3 py-1">
                <span className="text-off-white text-sm">{highlightedTactic.mapName}</span>
              </div>
              
              {/* Overlay gradient */}
              <div className="absolute inset-0 bg-gradient-to-t from-gunmetal to-transparent lg:bg-gradient-to-r" />
            </div>
          </div>
          
          {/* Right side - Content */}
          <div className="lg:col-span-2 p-6 lg:p-8 flex flex-col">
            <div className="mb-4 flex items-center">
              <div className="w-10 h-10 rounded-full bg-olive-drab flex items-center justify-center mr-3">
                <span className="text-off-white font-bold">{highlightedTactic.author.charAt(0)}</span>
              </div>
              <div>
                <span className="block text-off-white font-medium">{highlightedTactic.author}</span>
                <span className="text-off-white/60 text-sm">
                  {new Date(highlightedTactic.createdAt).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric'
                  })}
                </span>
              </div>
            </div>
            
            <h3 className="text-2xl font-bold text-olive-drab mb-3">{highlightedTactic.title}</h3>
            
            <p className="text-off-white/80 mb-6">{highlightedTactic.description}</p>
            
            <div className="flex flex-wrap gap-2 mb-6">
              {highlightedTactic.vehicleTypes.map((type) => (
                <span 
                  key={type} 
                  className="text-xs bg-deep-blue/30 text-off-white rounded-full px-2 py-1"
                >
                  {type}
                </span>
              ))}
            </div>
            
            <div className="flex items-center space-x-4 mb-6">
              <div className="flex items-center">
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  className="h-5 w-5 text-burnt-orange mr-1" 
                  fill="none" 
                  viewBox="0 0 24 24" 
                  stroke="currentColor"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
                </svg>
                <span className="text-burnt-orange font-medium">{highlightedTactic.upvotes}</span>
              </div>
              
              <div className="flex items-center">
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  className="h-5 w-5 text-deep-blue mr-1" 
                  fill="none" 
                  viewBox="0 0 24 24" 
                  stroke="currentColor"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
                <span className="text-deep-blue font-medium">{highlightedTactic.downvotes}</span>
              </div>
            </div>
            
            <div className="mt-auto">
              <Link 
                href={`/tactics/${highlightedTactic.slug}`}
                className="inline-flex items-center px-4 py-2 bg-burnt-orange text-off-white rounded hover:bg-burnt-orange/90 transition"
              >
                View Full Strategy
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  className="h-5 w-5 ml-2" 
                  fill="none" 
                  viewBox="0 0 24 24" 
                  stroke="currentColor"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </Link>
            </div>
          </div>
        </div>
      </div>
      
      <div className="mt-8 text-center">
        <Link 
          href="/signup" 
          className="inline-flex items-center px-6 py-3 bg-deep-blue text-off-white rounded-md hover:bg-deep-blue/90 transition"
        >
          Join the Community to Contribute
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            className="h-5 w-5 ml-2" 
            fill="none" 
            viewBox="0 0 24 24" 
            stroke="currentColor"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
          </svg>
        </Link>
      </div>
    </Section>
  );
} 