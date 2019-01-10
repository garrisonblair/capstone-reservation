import React, { Component } from 'react';
import { Button, List, Icon } from 'semantic-ui-react';
import PropTypes from 'prop-types';

class MemberRowItem extends Component {
  handleDeletion = () => {
    const { deleteFunction, selectedMember } = this.props;
    deleteFunction(selectedMember.user.id);
  }

  render() {
    const { selectedMember, isAdmin } = this.props;
    return (
      <List.Item>

        <List.Content floated="left">
          <h3>
            <Icon name="envelope" />
            {selectedMember.user.username}
          </h3>
        </List.Content>
        <List.Content floated="right">
          {isAdmin ? <Button onClick={this.handleDeletion}>Remove</Button> : ''}
        </List.Content>
      </List.Item>
    );
  }
}

MemberRowItem.propTypes = {
  // eslint-disable-next-line react/forbid-prop-types
  selectedMember: PropTypes.object.isRequired,
  deleteFunction: PropTypes.func.isRequired,
  isAdmin: PropTypes.bool.isRequired,
};

export default MemberRowItem;
