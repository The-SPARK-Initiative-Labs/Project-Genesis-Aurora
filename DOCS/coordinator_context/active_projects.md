# Active Coordination Projects

## Side Project: Context Agent
**Goal**: Create specialized AI that manages context files automatically
**Status**: New idea for tomorrow
**Concept**: 
- Dedicated AI that reads, updates, and maintains all context files
- Could automate context management for coordinators and coding AIs
- Another layer of AI-native development automation
- Would fit into the coordinator → coding AI → context agent workflow
- **BRAINSTORM NEEDED**: How would it read our conversation? Integration method unclear
- Could use local LM Studio model for this
- **HUGE POTENTIAL**: Frees up conversation tokens for actual work

## Side Project: Document Translation System
**Goal**: Convert human-readable docs to AI-optimized format
**Status**: Planning phase
**Details**:
- Ben created `sdk_dev_guide.json` as proof of concept
- Need to develop translation process for other docs
- I should design optimal formats for coding agents (not just copy Ben's JSON structure)
- Consider combining multiple docs into single onboarding doc

## Side Project: DOCS Folder Restructure
**Goal**: Organize documentation for different roles and purposes
**Status**: Folders created
**Completed Structure**:
- `/research/` - Raw research to extract insights, then archive
- `/sdk_reference/` - Clean technical specs for coding agents
- `/coordinator_context/` - Deep context docs for coordinators
- `/archive/` - Processed research docs

**Next Steps**: Move existing docs to appropriate folders

**Questions to Resolve**:
- Role-specific master docs vs unified docs?
- How to handle updates when Aurora changes?
- Testing documentation placement?

## Side Project: Coordinator Onboarding System
**Goal**: Create systematic onboarding for future coordinators
**Status**: Complete
**Completed**:
- Created `coordinator_context/` folder structure
- Built `coordinator_onboarding.md` with systematic onboarding steps
- Created persistent context files (state, decisions, insights, ben_preferences)
- Enables picking up where we left off after conversation resets
- Includes working relationship with Ben and coordinator responsibilities

## Side Project: Improved Coding Onboarding
**Goal**: Streamline coding AI onboarding after coordinator system is built
**Status**: Future work
**Concept**:
- Coding AIs don't need deep Aurora context like coordinators
- Focus on implementation tasks only
- Single master technical reference doc
