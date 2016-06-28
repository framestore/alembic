#include <Alembic/AbcCoreLayer/ArImpl.h>
#include <Alembic/AbcCoreFactory/IFactory.h>
#include <Alembic/AbcCoreLayer/OrImpl.h>

namespace Alembic {
namespace AbcCoreLayer {
namespace ALEMBIC_VERSION_NS {

//-*****************************************************************************
ArImpl::ArImpl( ArchiveReaderPtrs & iArchives )
{
    m_archiveVersion = -1;
    m_header.reset( new AbcA::ObjectHeader() );
    m_archives.reserve( iArchives.size() );
    ArchiveReaderPtrs::iterator it = iArchives.begin();

    for ( ; it != iArchives.end(); ++it )
    {
        // bad archive ptr?  skip to the next one
        if ( !( *it ) )
        {
            continue;
        }

        m_archives.push_back( *it );

        if ( !m_fileName.empty() )
        {
            m_fileName += ",";
        }
        m_fileName += (*it)->getName();

        // go over this archives time samplings and add them to our list
        Util::uint32_t numSamplings = (*it)->getNumTimeSamplings();
        for ( Util::uint32_t i = 0; i < numSamplings; ++i )
        {
            Util::uint32_t j = 0;
            for ( j = 0; j < m_timeSamples.size(); ++j )
            {
                if ( m_timeSamples[j] == (*it)->getTimeSampling( i ) )
                {
                    break;
                }
            }

            // it wasn't found, add it and the max samples
            if ( j == m_timeSamples.size() )
            {
                m_timeSamples.push_back( (*it)->getTimeSampling( i ) );
                m_maxSamples.push_back(
                    (*it)->getMaxNumSamplesForTimeSamplingIndex( i ) );
            }
            else
            {
                m_maxSamples[j] = std::max( m_maxSamples[j],
                    (*it)->getMaxNumSamplesForTimeSamplingIndex( i ) );
            }
        }

        // the data stored in the top level meta data is special
        // lets combine them all together
        const AbcA::MetaData & md = (*it)->getMetaData();
        AbcA::MetaData::const_iterator mit;
        for ( mit = md.begin(); mit != md.end(); ++mit )
        {
            std::string val = m_header->getMetaData().get( mit->first );
            if ( !val.empty() )
            {
                val += " , ";
            }
            val += mit->second;
            m_header->getMetaData().set( mit->first, val );
        }

        m_archiveVersion = std::max( m_archiveVersion,
                                     (*it)->getArchiveVersion() );
    }
}

//-*****************************************************************************
ArImpl::~ArImpl()
{

}

//-*****************************************************************************
const std::string &ArImpl::getName() const
{
    return m_fileName;
}

//-*****************************************************************************
const AbcA::MetaData & ArImpl::getMetaData() const
{
    return m_header->getMetaData();
}

//-*****************************************************************************
AbcA::ObjectReaderPtr ArImpl::getTop()
{

    std::vector< AbcA::ObjectReaderPtr > tops;
    tops.reserve( m_archives.size() );
    ArchiveReaderPtrs::iterator arItr = m_archives.begin();
    for ( ; arItr != m_archives.end(); ++arItr )
    {
        tops.push_back( (*arItr)->getTop() );
    }

    return OrImplPtr( new OrImpl( shared_from_this(), tops, m_header ) );
}

//-*****************************************************************************
AbcA::TimeSamplingPtr ArImpl::getTimeSampling( Util::uint32_t iIndex )
{
    if( iIndex < m_timeSamples.size() )
    {
        return m_timeSamples[ iIndex ];
    }

    return AbcA::TimeSamplingPtr();
}

//-*****************************************************************************
AbcA::ArchiveReaderPtr ArImpl::asArchivePtr()
{
    return shared_from_this();
}

//-*****************************************************************************
AbcA::index_t
ArImpl::getMaxNumSamplesForTimeSamplingIndex( Util::uint32_t iIndex )
{
    if( iIndex < m_maxSamples.size() )
    {
        return m_maxSamples[iIndex];
    }

    return 0;
}

//-*****************************************************************************
AbcA::ReadArraySampleCachePtr ArImpl::getReadArraySampleCachePtr()
{
    return AbcA::ReadArraySampleCachePtr();
}

//-*****************************************************************************
void ArImpl::setReadArraySampleCachePtr( AbcA::ReadArraySampleCachePtr iPtr )
{
    // don't even bother
}

//-*****************************************************************************
Util::uint32_t ArImpl::getNumTimeSamplings()
{
    return m_timeSamples.size();
}

//-*****************************************************************************
Util::int32_t ArImpl::getArchiveVersion()
{
    return m_archiveVersion;
}

} // End namespace ALEMBIC_VERSION_NS
} // End namespace AbcCoreOgawa
} // End namespace Alembic
