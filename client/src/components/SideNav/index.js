import React, { Component } from 'react';
import { withRouter } from 'react-router-dom';
import PropTypes from 'prop-types';
import './SideNav.scss';


class SideNav extends Component {
  render() {
    const { selectedMenu, navConfig, history } = this.props;
    return (
      <div className="sidenav">
        <ul>
          {navConfig.map(row => (
            <li
              className={selectedMenu === row.menu ? 'active' : ''}
              onClick={function () { history.push(row.path); }}
              key={row.menu}
            >
              {row.text}
            </li>))}
        </ul>
      </div>
    );
  }
}

SideNav.propTypes = {
  selectedMenu: PropTypes.string.isRequired,
  navConfig: PropTypes.array.isRequired,
};

export default withRouter(SideNav);
