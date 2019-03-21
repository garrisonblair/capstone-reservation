import React, { Component } from 'react';
import './Groups.scss';
import GroupsTable from './GroupTable';


// eslint-disable-next-line react/prefer-stateless-function
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
