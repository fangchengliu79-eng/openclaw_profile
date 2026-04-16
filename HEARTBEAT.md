# HEARTBEAT.md - Periodic Checks for Forest

## Purpose
This file defines periodic checks Grove performs during heartbeats. When nothing needs attention, respond with NO_REPLY (not HEARTBEAT_OK).

## Check Schedule
- **Frequency:** Every 30-60 minutes during working hours (08:00-20:00 Asia/Shanghai)
- **Weekends:** Reduced frequency (every 2-3 hours)
- **Night:** Minimal checks (23:00-08:00) unless urgent

## Check Items

### 1. Email Priority Check
- Check for urgent business emails
- Flag compliance-related communications
- Monitor German HQ communications

### 2. System Status Check
- Verify critical infrastructure status
- Check backup completion status
- Monitor security alerts

### 3. Calendar Review
- Upcoming meetings in next 2 hours
- Important deadlines in next 24 hours
- Compliance audit schedules

### 4. Project Milestones
- Upcoming project deliverables
- Integration testing schedules
- Documentation deadlines

## Response Protocol

### Reach Out When:
- Urgent email requiring immediate attention
- Calendar event starting within 30 minutes
- System alert requiring intervention
- Compliance deadline approaching (<24h)

### Stay Silent (Respond with NO_REPLY) When:
- No urgent items detected
- Forest appears busy or in meetings
- Late night/early morning hours
- Recent interaction (<30 minutes)

## Notes
- Respect working hours and focus time
- Prioritize business-critical notifications
- Maintain professional, concise communication
- Document checks in memory/heartbeat-state.json
