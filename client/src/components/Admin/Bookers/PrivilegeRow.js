import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Button, List } from 'semantic-ui-react';

class PrivilegeRow extends Component {
  handleRemovePrivilege = () => {

  }

  render() {
    const { privilege } = this.props;
    console.log(privilege);
    return (
      <List.Item>
        <List.Content floated="right">
          <Button>Remove</Button>
        </List.Content>
        <List.Content>
          {privilege.name}
        </List.Content>
      </List.Item>
    );
  }
}

PrivilegeRow.propTypes = {
  // eslint-disable-next-line react/forbid-prop-types
  privilege: PropTypes.object.isRequired,
};

export default PrivilegeRow;
