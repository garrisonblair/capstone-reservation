import React, { Component } from 'react';
import { Button, List } from 'semantic-ui-react';
import PropTypes from 'prop-types';

class MemberRowItem extends Component {
  state = {
    member: '',
  }

  componentDidMount() {
    const { selectedMember } = this.props;
    this.setState({
      member: selectedMember,
    });
  }

  handleDeletion = () => {
    const { member } = this.state;
    // eslint-disable-next-line react/prop-types
    const { deleteFunction } = this.props;
    deleteFunction(member);
  }

  render() {
    const { member } = this.state;
    return (
      <List.Item>
        <List.Content floated="left">
          <h2>{member}</h2>
        </List.Content>
        <List.Content floated="right">
          <Button onClick={this.handleDeletion}>Remove</Button>
        </List.Content>
      </List.Item>
    );
  }
}

MemberRowItem.propTypes = {
  selectedMember: PropTypes.string,
};

MemberRowItem.defaultProps = {
  selectedMember: null,
};

export default MemberRowItem;
