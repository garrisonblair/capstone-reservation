import React, { Component } from 'react';
// import PropTypes from 'prop-types';
import { Button, Table } from 'semantic-ui-react';
// import api from '../../utils/api';
import GroupsModal from './GroupsModal';
// import sweetAlert from 'sweetalert2';


class GroupsRowItem extends Component {
  state = {
    openModal: false,
  }

  openModal = () => {
    this.setState({ openModal: true });
  }

  closeModal = () => {
    // const { syncRoomList } = this.props;
    // syncRoomList();
    this.setState({ openModal: false });
  }
  componentDidMount(){
      console.log('mounted')
  }

  render() {
    const { group } = this.props;
    const { openModal } = this.state;
    return (
      <Table.Row key={group.id}>
        <Table.Cell textAlign="center"><h4>{group.name}</h4></Table.Cell>
        <Table.Cell textAlign="center">
          <Button icon="edit" onClick={this.openModal} />
        </Table.Cell>
        {/* <GroupsModal
          show={openModal}
          selectedRoom={room}
          onClose={this.closeModal}
        /> */}
      </Table.Row>
    );
  }
}

// GroupsRowItem.propTypes = {

// };

export default GroupsRowItem;
