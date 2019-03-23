import React, { Component } from 'react';
import { withRouter } from 'react-router-dom';
import './Groups.scss';
import GroupsTable from './GroupTable';
import queryParams from '../../../utils/queryParams';


// eslint-disable-next-line react/prefer-stateless-function
class Groups extends Component {
  state = {
    groupID: null,
  }

  componentWillMount() {
    // eslint-disable-next-line react/prop-types
    const { location } = this.props;

    const params = queryParams.parse(location.search);
    this.setState({ groupID: params.group });
  }

  render() {
    const { groupID } = this.state;
    return (
      <div id="admin-groups">
        <h1>Groups</h1>
        <GroupsTable selectedGroup={groupID} />
      </div>
    );
  }
}

export default withRouter(Groups);
