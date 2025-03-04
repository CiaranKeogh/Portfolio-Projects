from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine, Text, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from ..config.config import DB_PATH

# Create SQLAlchemy base
Base = declarative_base()

def get_engine():
    """Create and return a database engine"""
    return create_engine(f"sqlite:///{DB_PATH}")

def get_session():
    """Create and return a database session"""
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

class VMP(Base):
    """Virtual Medicinal Product"""
    __tablename__ = 'vmp'
    
    VPID = Column(Integer, primary_key=True)
    DESC = Column(String(255))
    
    # Relationships
    vmpps = relationship("VMPP", back_populates="vmp")
    amps = relationship("AMP", back_populates="vmp")

class VMPP(Base):
    """Virtual Medicinal Product Pack"""
    __tablename__ = 'vmpp'
    
    VPPID = Column(Integer, primary_key=True)
    VPID = Column(Integer, ForeignKey('vmp.VPID'))
    DESC = Column(String(255))
    
    # Relationships
    vmp = relationship("VMP", back_populates="vmpps")
    ampps = relationship("AMPP", back_populates="vmpp")

class AMP(Base):
    """Actual Medicinal Product"""
    __tablename__ = 'amp'
    
    APID = Column(Integer, primary_key=True)
    VPID = Column(Integer, ForeignKey('vmp.VPID'))
    DESC = Column(String(255))
    
    # Relationships
    vmp = relationship("VMP", back_populates="amps")
    ampps = relationship("AMPP", back_populates="amp")

class AMPP(Base):
    """Actual Medicinal Product Pack"""
    __tablename__ = 'ampp'
    
    APID = Column(Integer, primary_key=True)
    VPPID = Column(Integer, ForeignKey('vmpp.VPPID'))
    DESC = Column(String(255))
    PRICE = Column(Float, nullable=True)
    PRICE_SOURCE = Column(String(20))  # 'initial' or 'calculated'
    PRICE_METHOD = Column(String(50), nullable=True)  # e.g., 'Same VMPP', 'Same VMP'
    
    # Relationships
    vmpp = relationship("VMPP", back_populates="ampps")
    amp = relationship("AMP", back_populates="ampps")
    gtins = relationship("GTIN", back_populates="ampp")

class GTIN(Base):
    """Global Trade Item Number"""
    __tablename__ = 'gtin'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    GTIN = Column(String(14))
    APID = Column(Integer, ForeignKey('ampp.APID'))
    
    # Relationships
    ampp = relationship("AMPP", back_populates="gtins")
    
    # Indexes
    __table_args__ = (
        Index('idx_gtin_gtin', GTIN),
        Index('idx_gtin_apid', APID),
    )

class SearchData(Base):
    """Unified search table"""
    __tablename__ = 'search_data'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    VPPID = Column(Integer, ForeignKey('vmpp.VPPID'))
    VMPP = Column(String(255))
    VPID = Column(Integer, ForeignKey('vmp.VPID'))
    VMP = Column(String(255))
    APID = Column(Integer, ForeignKey('ampp.APID'))
    Description = Column(String(255))
    Brand_or_Generic = Column(String(20))
    Drug_Tariff_Price = Column(Float)
    Price_Source = Column(String(20))
    Price_Method = Column(String(50), nullable=True)
    
    # Indexes
    __table_args__ = (
        Index('idx_search_vppid', VPPID),
        Index('idx_search_apid', APID),
        Index('idx_search_description', Description),
    )

def init_db():
    """Initialize the database by creating all tables"""
    engine = get_engine()
    Base.metadata.create_all(engine)
    return engine 