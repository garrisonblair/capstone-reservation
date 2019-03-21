import React, { Component } from 'react';
// import {
//   Table, Segment, Pagination, Form, Button, Dropdown, Message, Icon,
// } from 'semantic-ui-react';
import './Groups.scss';
// import api from '../../../utils/api';
import GroupsTable from './GroupTable';


class Groups extends Component {
  render() {
    // const { groups } = this.state;
    // console.log(groups);
    return (
      <div id="admin-groups">
        <h1>Groups</h1>
        <GroupsTable />
      </div>
    );
  }
}

export default Groups;
