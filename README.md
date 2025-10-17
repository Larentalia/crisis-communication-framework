# Crisis Communication Framework

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

A practical, field-tested framework for managing organizational crises across media and social channels. Based on real-world implementation in highly regulated environments and aligned with UK Government Crisis Communications Operating Model principles.

## 🚀 Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Basic Usage
See the [tools directory](tools/) for Python scripts that automate crisis reporting.

## 🎯 Purpose

This framework provides:
- **Crisis classification and severity assessment**
- **Response protocols by crisis type and level**
- **Detection and early warning systems**
- **Communication templates and playbooks**
- **Stakeholder coordination guidelines**
- **Post-crisis analysis methodology**

Designed for communications professionals, crisis managers, and organizations seeking to build robust crisis preparedness capabilities.

---

## 📊 Crisis Classification

Based on the [UK Government Crisis Communications Operating Model](https://www.communications.gov.uk/wp-content/uploads/2023/05/Crisis-Communications-Operating-Model.pdf), crises are classified into three levels:

### Level 1: Significant Emergency
- **Impact:** Localized incident affecting specific departments or regions
- **Response time:** < 2 hours
- **Coordination:** Departmental level
- **Examples:** Local service disruption, minor data breach, isolated severe weather impact

### Level 2: Serious Emergency
- **Impact:** Regional or multi-departmental impact requiring coordinated response
- **Response time:** < 1 hour
- **Coordination:** Cross-departmental with executive awareness
- **Examples:** Major cybersecurity incident, significant operational failure, reputational attack

### Level 3: Catastrophic Emergency
- **Impact:** Organization-wide or national-level crisis
- **Response time:** < 30 minutes
- **Coordination:** Executive-led crisis team with full organizational mobilization
- **Examples:** Global pandemic, major leadership crisis, catastrophic system failure

---

## 🚨 Crisis Types & Response Playbooks

### 1. Cybersecurity Incident
**Common scenarios:** Data breach, ransomware attack, system compromise, DDoS attack

**Key considerations:**
- Legal and regulatory obligations (GDPR, data protection laws)
- Customer data exposure risk
- Service continuity impact
- Coordination with IT, legal, and regulatory teams

**Initial response priorities:**
1. Contain the incident (IT-led)
2. Assess data exposure scope
3. Notify regulatory authorities (if required by law)
4. Prepare holding statement
5. Monitor social/media for misinformation

**Communication approach:**
- Transparency within legal constraints
- Focus on actions being taken
- Clear timelines for updates
- Dedicated incident response page

---

### 2. Public Health Emergency
**Common scenarios:** Pandemic, outbreak affecting operations, health and safety incident

**Key considerations:**
- Employee safety first
- Government guidance alignment
- Operational continuity
- Customer/public safety communication

**Initial response priorities:**
1. Activate business continuity protocols
2. Align messaging with public health authorities
3. Communicate safety measures to employees
4. Update customers on service impacts
5. Monitor for misinformation about organizational response

**Communication approach:**
- Empathy and care-first messaging
- Clear, factual information
- Regular updates on safety measures
- Support resources for affected stakeholders

---

### 3. Severe Weather / Natural Disaster
**Common scenarios:** Hurricanes, floods, extreme weather events impacting operations

**Key considerations:**
- Employee and customer safety
- Service disruption extent
- Geographic impact zones
- Recovery timeline

**Initial response priorities:**
1. Account for employee safety
2. Assess operational impact
3. Communicate service disruptions
4. Coordinate with emergency services
5. Provide recovery timeline estimates

**Communication approach:**
- Safety-first messaging
- Clear service impact information
- Alternative contact methods
- Community support initiatives

---

### 4. Reputational Crisis
**Common scenarios:** Misinformation campaigns, coordinated negative attacks, viral negative content, brand hijacking

**Key considerations:**
- Speed of spread (especially on social media)
- Fact vs. fiction assessment
- Amplification risk
- Long-term brand impact

**Initial response priorities:**
1. Verify facts immediately
2. Assess sentiment and spread velocity
3. Identify inorganic activity (bots, coordinated campaigns)
4. Prepare fact-based response
5. Monitor all channels continuously

**Communication approach:**
- Rapid response (minutes, not hours)
- Fact-correction with evidence
- Avoid amplifying false narratives
- Direct engagement when appropriate
- Consider when silence is strategic

---

### 5. Service/Operations Disruption
**Common scenarios:** System outages, supply chain failures, major service interruptions

**Key considerations:**
- Customer impact scope
- Service restoration timeline
- Compensation/resolution approach
- Regulatory reporting requirements

**Initial response priorities:**
1. Acknowledge the issue immediately
2. Provide known information
3. Set expectations for updates
4. Coordinate with operations team
5. Monitor customer sentiment

**Communication approach:**
- Acknowledge, apologize, act
- Transparency about timeline
- Regular updates (even if "no new information")
- Clear restoration milestones
- Post-incident follow-up

---

### 6. Leadership & Executive Crisis
**Common scenarios:** Executive death/serious incident, legal investigations, misconduct allegations, succession crises

**Key considerations:**
- Legal implications and restrictions
- Employee morale and uncertainty
- Market/investor confidence (if public company)
- Media pressure intensity
- Family/personal privacy
- Regulatory obligations

**Initial response priorities:**
1. Coordinate with legal counsel immediately
2. Assess what can/cannot be communicated legally
3. Prepare internal communication first (employees before external)
4. Brief board/senior leadership
5. Designate authorized spokesperson
6. Monitor for speculation and misinformation

**Communication approach:**
- Extreme sensitivity and respect
- Legal review of all statements
- Tiered communication (internal → investors → public)
- Limited, factual information only
- "We cannot comment on ongoing investigations" when appropriate
- Demonstrate organizational stability and continuity

**Special considerations:**
- **Death/bereavement:** Compassion first, operational continuity second
- **Legal investigations:** Coordinate with legal team, respect presumption of innocence
- **Misconduct allegations:** Balance transparency with fair process
- **Succession crisis:** Reassure stakeholders of continuity and governance

---

## 🔍 Detection & Early Warning

### Monitoring Strategy

**Media Monitoring:**
- Traditional news outlets
- Trade publications
- Regional/local media
- Broadcast media

**Social Media Listening:**
- Brand mentions (direct and indirect)
- Executive name monitoring
- Industry-relevant keywords
- Sentiment analysis
- Volume spike alerts

**Red Flags:**
- Sudden volume increase (>200% normal baseline)
- Sentiment shift (positive to negative)
- Inorganic activity patterns (bot networks)
- Coordinated messaging
- Verified account amplification
- Mainstream media pickup of social narrative

### Alert Thresholds

**Tier 1 - Monitor:** Elevated activity, no immediate action
**Tier 2 - Notify:** Brief crisis team, prepare holding statements
**Tier 3 - Activate:** Immediate response required

---

## 📋 Response Protocols

### First 30 Minutes
1. **Verify:** Confirm incident details
2. **Assess:** Determine crisis level (1-3)
3. **Activate:** Notify crisis team
4. **Contain:** Take immediate action to limit damage
5. **Prepare:** Draft holding statement

### First 2 Hours
1. **Communicate internally:** Brief employees
2. **Communicate externally:** Issue initial statement
3. **Monitor:** Track response and emerging narratives
4. **Coordinate:** Align with legal, operations, HR as needed
5. **Plan:** Develop ongoing communication strategy

### First 24 Hours
1. **Update:** Provide new information as available
2. **Engage:** Respond to key stakeholders
3. **Analyze:** Track sentiment and reach
4. **Adjust:** Refine messaging based on response
5. **Document:** Record all actions and decisions

---

## 💬 Communication Templates

### Holding Statement Template
```
We are aware of [incident description]. The safety and wellbeing of [affected parties] 
is our top priority. We are currently [actions being taken] and will provide updates 
as more information becomes available. For immediate concerns, please contact 
[appropriate channel].
```

### Update Statement Template
```
Update on [incident]: [New information]. We have [actions taken] and are continuing 
to [ongoing actions]. We expect [timeline/next steps]. Thank you for your patience 
and understanding.
```

### Resolution Statement Template
```
Following [incident], we can confirm that [resolution]. We have [corrective actions] 
to prevent recurrence. We apologize for [impact] and thank [stakeholders] for 
[response/support]. For questions, please contact [channel].
```

---

## 🗺️ Stakeholder Mapping

### Primary Stakeholders (Always notify)
- **Employees:** First to know, internal channels
- **Customers/Users:** Direct impact, immediate notification
- **Regulators:** Legal obligations, formal notification
- **Leadership/Board:** Executive briefing, decision authority

### Secondary Stakeholders (Situational)
- **Media:** Proactive or reactive depending on severity
- **Partners/Vendors:** If operational impact affects them
- **Investors:** Public companies, material impact
- **Community:** Local incidents, social responsibility

### Communication Channels by Stakeholder
- **Internal:** Email, intranet, team meetings, leadership briefings
- **Customers:** Social media, website, email, SMS, app notifications
- **Media:** Press releases, media statements, spokesperson interviews
- **Regulators:** Formal notifications per legal requirements

---

## 📈 Post-Crisis Analysis

### Debrief Framework (Within 72 hours)

**What happened:**
- Timeline of events
- Initial detection method
- Response activation time

**What worked:**
- Effective protocols
- Successful communications
- Team coordination strengths

**What didn't work:**
- Protocol gaps
- Communication delays
- Resource constraints

**Lessons learned:**
- Process improvements
- Training needs
- Template updates
- Technology enhancements

### Metrics to Track
- Time to detection
- Time to first response
- Stakeholder reach
- Sentiment analysis
- Media coverage (volume, tone, reach)
- Resolution time
- Customer/employee feedback

---

## 🛠️ Tools & Resources

### Monitoring Tools
- Social listening platforms (Sprout Social, Brandwatch, Hootsuite)
- Media monitoring services
- Google Alerts
- Internal reporting systems

### Communication Platforms
- Mass notification systems
- Social media management tools
- Email distribution systems
- Crisis communication hotlines

### Documentation
- [UK Government Crisis Communications Operating Model](https://www.communications.gov.uk/wp-content/uploads/2023/05/Crisis-Communications-Operating-Model.pdf)
- Industry-specific regulatory guidelines
- Legal counsel contact protocols

---

## 🤝 Contributing

This framework is based on real-world crisis management experience. Contributions, suggestions, and adaptations are welcome. Please open an issue or submit a pull request.

---

## 📄 License

MIT License - Free to use and adapt for your organization's needs.

---

## ✍️ Author

**Begoña Penón**  
Crisis Communication & Reputational Risk Management Specialist  
[LinkedIn](https://www.linkedin.com/in/begopenon) | [GitHub](https://github.com/Larentalia)

*Developed based on 9+ years managing corporate communications in highly regulated environments, including real-world crisis response during cybersecurity incidents, public health emergencies, and severe weather events.*

---

## 🇪🇸 Versión en Español

Una versión completa en español de este framework está disponible bajo petición a la autora.
