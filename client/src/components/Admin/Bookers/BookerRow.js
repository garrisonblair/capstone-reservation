import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Table, Button } from 'semantic-ui-react';
import BookerModal from './BookerModal';


class BookerRow extends Component {
  state = {
    openModal: false,
  }

  onClickEditButton = () => {
    this.setState({ openModal: true });
  }

  closeModal = () => {
    const { syncBookers } = this.props;

    this.setState({ openModal: false });
    syncBookers();
  }

  render() {
    const { booker } = this.props;
    const { openModal } = this.state;
    console.log(booker);
    return (
      <Table.Row key={booker.username}>
        <Table.Cell textAlign="center">
          {booker.user.username}
        </Table.Cell>
        <Table.Cell>
          <Button icon="edit" className="edit-button" onClick={this.onClickEditButton} />
        </Table.Cell>
        <BookerModal
          show={openModal}
          booker={booker}
          onClose={this.closeModal}
        />
      </Table.Row>
    );
  }
}

BookerRow.propTypes = {
  // eslint-disable-next-line react/forbid-prop-types
  booker: PropTypes.object.isRequired,
  // eslint-disable-next-line react/no-unused-prop-types
  syncBookers: PropTypes.func.isRequired,
};
export default BookerRow;
