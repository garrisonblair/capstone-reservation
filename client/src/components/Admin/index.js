import React, { Component } from 'react';
import PropTypes from 'prop-types';
import AdminRequired from '../HOC/AdminRequired';
import SideNav from '../SideNav';
import './Admin.scss';


class Admin extends Component {

  componentDidMount = () => {
    document.title = 'Capstone Settings';
  }

  render() {
    const { content, menuType } = this.props;

    return (
      <div className="admin">
        <div className="admin__wrapper">
          <SideNav selectedMenu={menuType}/>
          <div className="admin__content">
            {content}
          </div>
        </div>
      </div>
    );
  }
}

Admin.propTypes = {
  menuType: PropTypes.string.isRequired,
  content: PropTypes.element.isRequired,
};

export default AdminRequired(Admin);
