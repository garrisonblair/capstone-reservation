import React, { Component } from 'react';
// import {
//   Table, Segment, Pagination, Form, Button, Dropdown, Message, Icon,
// } from 'semantic-ui-react';
import './Groups.scss';
import api from '../../../utils/api';


class Groups extends Component {
  state = {
    groups: [],
  }

  componentDidMount() {
    this.syncGroups();
  }

  syncGroups = () => {
    api.getMyGroups()
      .then((r) => {
        console.log(r);
      });
  }

  render() {
    const { groups } = this.state;
    console.log(groups);
    return (
      <div id="admin-groups">
        helo
      </div>
    );
  }
}

export default Groups;
