import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Table, Button } from 'semantic-ui-react';
import BookerModal from './BookerModal';


class BookerRow extends Component {
  state = {
    openModal: false,
  }

  render() {
    const { booker } = this.props;
    const { openModal } = this.state;
    return (
      <Table.Row key={booker.username}>
        <Table.Cell>
          {booker.username}
        </Table.Cell>
        <Table.Cell>
          <Button icon="edit" className="edit-button" onClick={this.onClickEditButton} />
        </Table.Cell>
        <BookerModal
          show={openModal}
          booker={booker}
        />
      </Table.Row>
    );
  }
}

BookerRow.propTypes = {
  // eslint-disable-next-line react/forbid-prop-types
  booker: PropTypes.object.isRequired,
};
export default BookerRow;
