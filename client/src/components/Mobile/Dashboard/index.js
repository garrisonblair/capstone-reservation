import React, { Component } from 'react';
import { Accordion, Icon } from 'semantic-ui-react';
import UserBookings from '../../UserBookings';
import Privileges from '../../Privileges';
import Groups from '../../Groups';
import GroupInvitations from '../../GroupInvitations';
import Profile from '../../Profile';

import './Dashboard.scss';


class MobileDashboard extends Component {
  state = {
    activeIndex: -1,
  };

  groupRef = React.createRef();

  syncGroups = () => {
    this.groupRef.current.syncGroups();
  };

  handleClickAccordion = (e, titleProps) => {
    const { index } = titleProps;
    const { activeIndex } = this.state;
    const newIndex = activeIndex === index ? -1 : index;
    this.setState({ activeIndex: newIndex });
  }

  render() {
    const { activeIndex } = this.state;

    return (
      <div className="mobile_dash">
        <Accordion fluid styled>
          <Accordion.Title active={activeIndex === 0} index={0} onClick={this.handleClickAccordion}>
            <Icon name="dropdown" />
            Current Reservations
          </Accordion.Title>
          <Accordion.Content active={activeIndex === 0}>
            <UserBookings vertical tabular={false} />
          </Accordion.Content>
          <Accordion.Title active={activeIndex === 1} index={1} onClick={this.handleClickAccordion}>
            <Icon name="dropdown" />
            Privileges
          </Accordion.Title>
          <Accordion.Content active={activeIndex === 1}>
            <Privileges />
          </Accordion.Content>
          <Accordion.Title active={activeIndex === 2} index={2} onClick={this.handleClickAccordion}>
            <Icon name="dropdown" />
            Groups
          </Accordion.Title>
          <Accordion.Content active={activeIndex === 2}>
            <Groups ref={this.groupRef} />
          </Accordion.Content>
          <Accordion.Title active={activeIndex === 3} index={3} onClick={this.handleClickAccordion}>
            <Icon name="dropdown" />
            Group Invitations
          </Accordion.Title>
          <Accordion.Content active={activeIndex === 3}>
            <GroupInvitations syncGroups={this.syncGroups} />
          </Accordion.Content>
          <Accordion.Title active={activeIndex === 4} index={4} onClick={this.handleClickAccordion}>
            <Icon name="dropdown" />
            Profile
          </Accordion.Title>
          <Accordion.Content active={activeIndex === 4}>
            <Profile />
          </Accordion.Content>
        </Accordion>
      </div>
    );
  }
}

export default MobileDashboard;
