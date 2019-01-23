import React, { Component } from 'react';
import { List, Icon, Button } from 'semantic-ui-react';
import PropTypes from 'prop-types';

class MemberRowItem extends Component {
  handleRemoveMember = () => {
    const { member, deleteFunction } = this.props;
    deleteFunction(member.id);
  }

  render() {
    const { member, isAdmin } = this.props;
    return (
      <List.Item>
        <List.Content floated="left">
          <h3>
            <Icon name="user" />
            {member.username}
          </h3>
        </List.Content>
        <List.Content floated="right">
          {isAdmin ? <Button onClick={this.handleRemoveMember}>Remove</Button> : ''}
        </List.Content>
      </List.Item>
    );
  }
}

MemberRowItem.propTypes = {
  // eslint-disable-next-line react/forbid-prop-types
  member: PropTypes.object.isRequired,
  deleteFunction: PropTypes.func.isRequired,
  isAdmin: PropTypes.bool.isRequired,
};
export default MemberRowItem;
