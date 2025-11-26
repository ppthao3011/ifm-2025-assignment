# Stock Portfolio Story Application

## Overview

This is a Streamlit-based stock portfolio visualization and reporting application. The system tracks a predefined portfolio of stocks across multiple sectors (Technology, Financial, Healthcare, Energy) and provides real-time portfolio analysis, performance metrics, and PDF report generation capabilities. The application fetches live stock data from Yahoo Finance and presents interactive visualizations using Plotly.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
**Technology Stack**: Streamlit web framework
- **Decision**: Uses Streamlit for rapid development of data-driven web applications
- **Rationale**: Streamlit provides native support for Python data visualization libraries and requires minimal frontend code
- **Key Features**: Wide layout mode for dashboard-style presentation, built-in caching mechanisms for performance optimization

### Data Visualization Layer
**Technology Stack**: Plotly (graph_objects and express modules)
- **Decision**: Plotly chosen for interactive charting capabilities
- **Rationale**: Provides rich, interactive visualizations that integrate seamlessly with Streamlit and Pandas dataframes
- **Use Cases**: Portfolio performance charts, sector allocation visualization, historical price tracking

### Data Processing
**Technology Stack**: Pandas and NumPy
- **Decision**: Standard Python data science stack for portfolio calculations
- **Rationale**: Industry-standard libraries for financial data manipulation and numerical computations
- **Responsibilities**: Portfolio metrics calculation (gains/losses, returns, allocations), data transformation for visualization

### Report Generation
**Technology Stack**: ReportLab
- **Decision**: PDF generation using ReportLab library
- **Rationale**: Provides programmatic PDF creation with precise control over layout and styling
- **Features**: Professional financial reports with tables, custom styling, and multi-page support
- **Components**: SimpleDocTemplate for document structure, Table/TableStyle for tabular data, Paragraph for text content

### Portfolio Data Model
**Architecture Pattern**: In-memory data structure
- **Decision**: Portfolio holdings defined as Python list of dictionaries in `PORTFOLIO_HOLDINGS`
- **Current State**: Static portfolio definition with 7 holdings across 4 sectors
- **Data Schema**: Each holding contains ticker symbol, company name, share quantity, purchase price, and sector classification
- **Limitation**: No persistent storage; portfolio changes require code modification
- **Future Consideration**: Could be migrated to database storage for dynamic portfolio management

### Caching Strategy
**Pattern**: Function-level caching with time-to-live (TTL)
- **Decision**: Streamlit's `@st.cache_data` decorator with 1-hour TTL
- **Rationale**: Reduces API calls to external services and improves application responsiveness
- **Applied To**: Stock price fetching and historical data retrieval functions
- **Trade-off**: Accepts slightly stale data (up to 1 hour) for better performance and reduced API rate limiting

## External Dependencies

### Stock Market Data Provider
**Service**: Yahoo Finance via yfinance Python library
- **Purpose**: Real-time and historical stock price data retrieval
- **Integration Points**: 
  - `fetch_current_prices()`: Retrieves latest closing prices for portfolio holdings
  - `fetch_historical_data()`: Fetches historical price data for performance analysis (function defined but implementation incomplete in provided code)
- **Data Accessed**: Stock ticker symbols, daily closing prices, historical price series
- **Error Handling**: Graceful degradation with None values for failed ticker lookups

### Python Package Dependencies
**Core Libraries**:
- **streamlit**: Web application framework and UI components
- **pandas**: Data manipulation and portfolio calculations
- **plotly**: Interactive visualization generation
- **numpy**: Numerical computations for financial metrics
- **yfinance**: Yahoo Finance API wrapper
- **reportlab**: PDF document generation
- **datetime**: Date/time handling for historical data queries

### No Database Currently Implemented
**Note**: The application currently operates entirely in-memory without persistent storage. Portfolio holdings are hardcoded in the application source. Future enhancements may add database integration (potentially PostgreSQL with Drizzle ORM) for:
- Persistent portfolio storage
- Historical transaction tracking
- User account management
- Custom portfolio creation